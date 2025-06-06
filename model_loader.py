from huggingface_hub import login
import torch
from PIL import Image
from transformers import LlavaProcessor,LlavaForConditionalGeneration,BitsAndBytesConfig
from .config import HUGGINGFACE_TOKEN


# 🔐 Login without prompting
login(token=HUGGINGFACE_TOKEN)

class ImageProcessor:
    def __init__(self,quantized=False):
        self.quantized = quantized
        self.model_id = "llava-hf/llava-1.5-7b-hf"
        self.processor = None
        self.model = None
        self.load_model()
    
    def load_model(self):

        self.processor = LlavaProcessor.from_pretrained(self.model_id)

        if self.quantized:
            # Quantization configuration for 4-bit
            quantization_config = BitsAndBytesConfig(
            load_in_8bit=True,
            device_map="mps",                 # Automatically assign GPUs/CPU
            offload_folder="offload_dir",
            )
            
            # Load quantized model
            self.model = LlavaForConditionalGeneration.from_pretrained(
                self.model_id,
                quantization_config=quantization_config,
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True,
                device_map="mps"
            )
        else :

            self.model = LlavaForConditionalGeneration.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16,
                low_cpu_mem_usage=False,
                device_map={"": "cpu"}, )
            
    def process_image(self,image_path:str,prompt:str="Describe this image in detail."):

        if self.quantized==False:
            device='cpu'
        else:
            device='mps'

        image = Image.open(image_path).convert('RGB')
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

        prompt = self.processor.apply_chat_template(conversation, add_generation_prompt=True)

        inputs = self.processor(images=image, text=prompt, return_tensors='pt')
        inputs = {k: v.to(device) for k, v in inputs.items()}

        for k,v in inputs.items():
            print(k,":",v.shape)

        # Generate response
        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_new_tokens=20,
                do_sample=True,
                temperature=0.7,
                pad_token_id=self.processor.tokenizer.eos_token_id,
                use_cache=True  
            )

        # Decode response
        response = self.processor.decode(
            output[0][inputs['input_ids'].shape[1]:], 
            skip_special_tokens=True
        )
            
        print("response",  response)

        return response

llm_service=ImageProcessor()

