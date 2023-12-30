from pydantic import BaseModel
from typing import List, Tuple


class BaseSDRequest(BaseModel):
    prompt: str
    encoded_control_net_image: str
    control_type: str
    height: int
    width: int
    controlnet_conditioning_scale: float = 1.0
    negative_prompt: str = "deformed, nsfw, blurr"
    base_model:str = "digiplay/Juggernaut_final"
    num_inference_steps: int = 20
    guidance_scale:float = 0.6
    num_images_per_prompt:int = 1
