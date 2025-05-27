import google.generativeai as genai
import os
from PIL import Image
from ..config import GOOGLE_AI_API_KEY


class GeminiImageAnalyzer:
    def __init__(self, api_key: str = None):
        """
        Initialize Gemini Image Analyzer
        
        Args:
            api_key: Google AI API key. If None, will try to get from environment
        """
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("Google AI API key is required. Set GOOGLE_AI_API_KEY env var or pass api_key parameter")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def _load_image(self, image_path: str) -> Image.Image:
        """Load and validate image"""
        try:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'P', 'L'):
                image = image.convert('RGB')
            
            return image
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            raise
    
    def generate_description(self, image_path: str, max_length: int = 200) -> str:
        try:
            image = self._load_image(image_path)
            
            prompt = f"""
            Analyze this image and provide a detailed, descriptive caption in {max_length} characters or less. 
            Focus on:
            - Main subjects and objects
            - Setting and environment
            - Colors and composition
            - Actions or activities
            - Mood or atmosphere

            Rules:
            - Avoid using starting line such as "Here is the description" or any other
            
            Write in a natural, engaging style as if describing the image to someone who cannot see it.
            """
            
            response = self.model.generate_content([prompt, image])
            description = response.text.strip()
            
            return description
            
        except Exception as e:
            return "Error generating image description"
    
    def generate_tags(self, image_path: str, max_tags: int = 3) -> str:
        try:
            image = self._load_image(image_path)
            
            prompt = f"""
            Analyze this image and generate up to {max_tags} relevant tags/keywords.
            
            Focus on:
            - Objects and subjects in the image
            - Activities or actions
            - genre
            - Emotions or mood
            
            Rules:
            - Use single words or short phrases (2-3 words max)
            - Must include one genre tag
            - Make tags specific and descriptive
            - Avoid generic tags like "image" or "photo"
            - Use lowercase
            - no duplicate tags
            - Separate with commas
            
            Example format: nature, mountains, sunset, landscape, peaceful, hiking, outdoor
            """
            
            response = self.model.generate_content([prompt, image])
            tags = response.text.strip()
            
            return tags
            
        except Exception as e:
            print(f"Error generating tags for {image_path}: {e}")
            return "image, photo, content"

try:
    gemini_analyzer = GeminiImageAnalyzer(GOOGLE_AI_API_KEY)
except ValueError as e:
    print(f"Gemini analyzer not initialized: {e}")
    gemini_analyzer = None

def generate_description(image_path: str) -> str:
    if gemini_analyzer is None:
        print("Gemini analyzer not available, returning default description")
        return "Image description not available - Gemini API not configured"
    
    return gemini_analyzer.generate_description(image_path)

def generate_tags(image_path: str) -> str:
    if gemini_analyzer is None:
        print("Gemini analyzer not available, returning default tags")
        return "image, photo, content"
    
    return gemini_analyzer.generate_tags(image_path)
