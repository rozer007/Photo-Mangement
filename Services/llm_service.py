from PIL import Image
import torch
from ..model_loader import model,processor

max_length = 200

prompt = f"""<|begin_of_text|><|start_header_id|>user<|end_header_id|>
<|image|>
Analyze this image and provide a detailed, descriptive caption in {max_length} characters or less. 
Focus on:
- Main subjects and objects
- Setting and environment
- Colors and composition
- Actions or activities
- Mood or atmosphere

Rules:
- Avoid using starting lines such as "Here is the description" or similar phrases.

Write in a natural, engaging style as if describing the image to someone who cannot see it.
<|start_header_id|>assistant<|end_header_id|>"""

prompt = f"""<|begin_of_text|><|start_header_id|>user<|end_header_id|>
<|image|>
Analyze this image and provide a detailed, descriptive caption in {max_length} characters or less.
<|start_header_id|>assistant<|end_header_id|>"""


def run():
    # Prepare inputs with prompt and image
    max_length = 200
    
    # Load and prepare image
    image = Image.open("uploads/1f888356-b912-4cb6-8da1-b1b721784f6c.jpg").convert("RGB")
    image = image.resize((512, 512))
    
    # Create the conversation messages format
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {
                    "type": "text", 
                    "text": "Describe this image briefly."
                }
            ]
        }
    ]

    input_text = processor.apply_chat_template(messages, add_generation_prompt=True)
    # input_text = "Describe this image briefly."
    print(input_text)

    inputs = processor(
    text=prompt,
    images=image,
    add_special_tokens=False,
    padding=True,
    return_tensors="pt").to(model.device)

    inputs = {k: v.to(model.device) if isinstance(v, torch.Tensor) else v for k, v in inputs.items()}


    # Debug: Print input shapes
    for k, v in inputs.items():
        if hasattr(v, 'shape'):
            print(f"{k}: {v.shape}")
        else:
            print(f"{k}: {type(v)}")


    with torch.no_grad():  # Add this for better memory management
        outputs = model.generate(
            **inputs, 
            max_new_tokens=100,  # Increased for better descriptions
            do_sample=True,
            temperature=0.7,
            pad_token_id=processor.tokenizer.eos_token_id,
            use_cache=False,  # Disable KV cache to save memory
            top_p=0.9,
            eos_token_id=processor.tokenizer.eos_token_id
        )

    input_len = inputs['input_ids'].shape[1]
    generated_tokens = outputs[0][input_len:]
    description = processor.decode(generated_tokens, skip_special_tokens=True)
    
    # return description.strip()
    # # Generate output tokens (model handles device internally)
    # outputs = model.generate(**inputs, max_new_tokens=30)  

    # # Decode the tokens to get the final description
    # description = processor.batch_decode(outputs[0])

    return description.strip()

# def run():
#     image_path = "uploads/1f888356-b912-4cb6-8da1-b1b721784f6c.jpg" 
#     image = Image.open(image_path).convert("RGB")
#     print(image)