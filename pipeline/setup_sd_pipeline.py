import torch
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from utils.control_net_utils import CONTROLNET_MAPPING

device = "cuda"
d_type = torch.float16
torch.cuda.empty_cache()


def setup_pipeline(base_model_path: str = "Yntec/epiCPhotoGasm"):

    control_type = "pose"
    controlnet = ControlNetModel.from_pretrained(CONTROLNET_MAPPING[control_type]["model_id"], torch_dtype=d_type).to(device)

    # Loading the base model with ControlNet
    pipe_control_net = StableDiffusionControlNetPipeline.from_pretrained(base_model_path,
                                                             controlnet=controlnet,
                                                             torch_dtype=torch.float16,
                                                             ).to(device)

    # load ip-adapter
    print("DEBUG: loading IP adapter ")
    return pipe_control_net


