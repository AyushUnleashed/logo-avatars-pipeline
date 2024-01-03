from pipeline.setup_sd_pipeline import setup_pipeline
from utils.image_utils import decode_base64_image, encode_image
from utils.control_net_utils import CONTROLNET_MAPPING
from models.base_request_model import BaseSDRequest
from diffusers.utils import load_image

import os


# Define global variables to track the loaded model paths & pipeline
current_model_path = None
current_control_type= None
pipe_control_net = None


def load_pipeline(model_path, control_type):
    global current_model_path, pipe_control_net,current_control_type
    if current_model_path != model_path or control_type != current_control_type:
        # Load the pipeline only if the model path or control type has changed
        pipe_control_net = setup_pipeline(base_model_path=model_path, control_type=control_type)
        current_model_path = model_path
        current_control_type = control_type

        print(f"\nChanging model to {model_path} & control_type to {control_type}\n")



def generate_image(base_request: BaseSDRequest,req_id):
    # Load the pipeline based on the model path in the request
    load_pipeline(base_request.base_model, base_request.control_type)

    # Decode the base64-encoded image
    control_net_image = decode_base64_image(base_request.encoded_control_net_image)

    # create control image for the pipeline using hinter
    control_image = CONTROLNET_MAPPING[base_request.control_type]["hinter"](control_net_image)

    print("DEBUG: before calling generate ")

    # saving the images array
    images = pipe_control_net(
        prompt=base_request.prompt,
        negative_prompt=base_request.negative_prompt,
        width=base_request.width,
        height=base_request.height,
        image=control_image,
        controlnet_conditioning_scale=base_request.controlnet_conditioning_scale,
        num_inference_steps=base_request.num_inference_steps,
        guidance_scale=base_request.guidance_scale,
    ).images

    # Extract the directory path for the final images
    directory = "assets/generations/output/"
    control_image_path = f"assets/generations/control_net/output_control_image_{req_id}.png"
    control_directory = os.path.dirname(control_image_path)

    # Create the directory and any missing parent directories if they don't exist
    os.makedirs(directory, exist_ok=True)
    os.makedirs(control_directory,exist_ok=True)

    # save controlnet image
    control_image.save(control_image_path)

    final_image_path = ""

    # Save each image in the list
    for i, image in enumerate(images):
        final_image_path = f"{directory}output_logo_{i}_{req_id}.png"
        image.save(final_image_path)
        image.save("output_logo_preview.png")

    # images[0].save("output_logo_preview.png")


    # send the path of last image
    return final_image_path


from utils.file_utils import delete_image_file

def run_generate(base_request: BaseSDRequest,req_id) -> str:
    final_image_path = generate_image(base_request, req_id)
    generated_image_encoded = encode_image(final_image_path)
    # once get it encoded, delete the file
    delete_image_file(final_image_path)
    return generated_image_encoded



def main():
    # generate mask
    logo_image_path = "../assets/sample_logo.png"
    control_net_image_path = logo_image_path

    prompt = "Colorful, jungle surrounding, trees, natural, detailed, hd, 4k"
    a_prompt = "best quality, extremely detailed"
    prompt = prompt + " "+ a_prompt

    negative_prompt = "ongbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality"

    control_type = "canny_edge"

    from utils.image_utils import encode_image

    encoded_control_net_image = encode_image(control_net_image_path)
    request = BaseSDRequest(prompt=prompt,
                            negative_prompt=negative_prompt,
                          control_type=control_type,
                          encoded_control_net_image=encoded_control_net_image,
                          height=512,
                          width=512)

    # Call the generate image function with the request
    generate_image(request,"1")

if __name__ == "__main__":
    main()