from transformers import BlipProcessor, BlipForQuestionAnswering
from PIL import Image
import torch

# Load model and processor only once
processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base").to("cpu")  # or "cuda"
model.eval()

def solve_math_from_image(image_path):
    """
    Takes an image path of a math equation and returns the answer using BLIP.
    """
    try:
        # Load and prepare image
        image = Image.open(image_path).convert("RGB")
        
        # Define the question
        question = "What is the result of the equation?"
        
        # Tokenize input
        inputs = processor(image, question, return_tensors="pt")
        
        # Generate prediction
        with torch.no_grad():
            output = model.generate(**inputs)
        
        # Decode and return answer
        answer = processor.decode(output[0], skip_special_tokens=True)
        return answer

    except Exception as e:
        return f"❌ Error: {str(e)}"