from PIL import Image
import time
import torch
from huggingface_hub import login
from transformers import LlavaProcessor, LlavaForConditionalGeneration,BitsAndBytesConfig
# from model_loader import model,processor

HUGGINGFACE_TOKEN='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'

# 🔐 Login without prompting
login(token=HUGGINGFACE_TOKEN)

model_id = "llava-hf/llava-1.5-7b-hf"
processor = LlavaProcessor.from_pretrained(model_id)

quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",  # better for accuracy
            bnb_4bit_compute_dtype=torch.float16)    
            # Load quantized model

model = LlavaForConditionalGeneration.from_pretrained(
    model_id,
    low_cpu_mem_usage=True,
    device_map="cpu",
    quantization_config=quantization_config,
    torch_dtype=torch.float16)

device='cpu'

image_path = "uploads/1f888356-b912-4cb6-8da1-b1b721784f6c.jpg"
image = Image.open(image_path).convert('RGB')

prompt="Describe this image in detail."

# Define a chat history and use `apply_chat_template` to get correctly formatted prompt
# Each value in "content" has to be a list of dicts with types ("text", "image") 
conversation = [
    {

      "role": "user",
      "content": [
           {"type": "text", "text": prompt},
           {"type": "image", "image": image}
        ],
    },
]
prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)

inputs = processor(images=image, text=prompt, return_tensors='pt')
inputs = {k: v.to(device) for k, v in inputs.items()}

for k,v in inputs.items():
    print(k,":",v.shape)

import datetime
now = datetime.datetime.now()

 # Generate response
with torch.no_grad():
    output = model.generate(
        **inputs,
        max_new_tokens=20,
        do_sample=True,
        temperature=0.7,
        pad_token_id=processor.tokenizer.eos_token_id,
        use_cache=True  
    )
    
# print(inputs['input_ids'].shape)

# Decode response
response = processor.decode(
    output[0][inputs['input_ids'].shape[1]:], 
    skip_special_tokens=True
)

then = datetime.datetime.now()

print(then-now)
 
print("response",  response)

# print("strip output",processor.decode(output[0][2:], skip_special_tokens=True))
