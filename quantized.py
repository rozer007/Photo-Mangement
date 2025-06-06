from PIL import Image
import torch
from huggingface_hub import login
from llama_cpp import Llama
from transformers import AutoProcessor, AutoModelForCausalLM
import io
# from model_loader import model,processor

HUGGINGFACE_TOKEN='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'

# 🔐 Login without prompting
login(token=HUGGINGFACE_TOKEN)

model_path = "llava_1.5_7b_Q8.gguf"
model = Llama(model_path=model_path)


image_path = "uploads/1f888356-b912-4cb6-8da1-b1b721784f6c.jpg"
image = Image.open(image_path).convert('RGB')

# prompt="Describe this image in detail."
# conversation = [
#     {

#       "role": "user",
#       "content": [
#            {"type": "text", "text": prompt},
#            {"type": "image", "image": image}
#         ],
#     },
# ]

# generation_kwargs = {
#     "max_tokens":200,
#     "echo":False,
#     "top_k":1
# }


# # response = llm.generate(images=image, text=prompt, **generation_kwargs)
# print(model.create_chat_completion(
# 	messages = "No input example has been defined for this model task."
# ))

buf = io.BytesIO()
image.save(buf, format='JPEG')
image_bytes = buf.getvalue()

   #    {"type": "image", "image": image_bytes}
prompt="Explain football"
messages = [
    {

      "role": "user",
      "content": [
           {"type": "text", "text": prompt}
        ],
    },
]

response = model.generate(prompt=messages, max_tokens=200, top_k=1)
print(response['choices'][0]['message']['content'])
