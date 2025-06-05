from huggingface_hub import login
from transformers import AutoProcessor,MllamaForConditionalGeneration

import torch
from .config import HUGGINGFACE_TOKEN

# 🔐 Login without prompting
login(token=HUGGINGFACE_TOKEN)

# ✅ Load model and processor only once
model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"

processor = AutoProcessor.from_pretrained(model_id)
model = MllamaForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="balanced",  # Automatically balance between GPU and CPU
    offload_folder="./offload",  # Offload some layers to disk
    low_cpu_mem_usage=True
) 
model.eval()  # Good practice