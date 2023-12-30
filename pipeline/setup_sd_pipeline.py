import torch
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from utils.control_net_utils import CONTROLNET_MAPPING
from utils.utils import DEFAULT_CONTROL_TYPE, DEFAULT_BASE_MODEL

device = "cuda"
d_type = torch.float16
pipe_control_net = None
torch.cuda.empty_cache()


def setup_pipeline(base_model_path: str = DEFAULT_BASE_MODEL, control_type: str = DEFAULT_CONTROL_TYPE):
    controlnet = ControlNetModel.from_pretrained(CONTROLNET_MAPPING[control_type]["model_id"], torch_dtype=d_type).to(
        device)

    # Loading the base model with ControlNet
    pipe_control_net = StableDiffusionControlNetPipeline.from_pretrained(base_model_path,
                                                                         controlnet=controlnet,
                                                                         torch_dtype=torch.float16,
                                                                         ).to(device)
    return pipe_control_net
