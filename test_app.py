from pipeline.generate_image import generate_image
from models.base_request_model import BaseSDRequest


def main():
    logo_image_path = "assets/sample_logo.png"
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
                            controlnet_conditioning_scale=2.0,
                            guidance_scale=4.0,
                            num_inference_steps=20,
                            height=512,
                            width=512)

    # Call the run_inpaint function with the request
    generate_image(request,"1")

if __name__ == "__main__":
    main()