import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_explanation(text: str, prompt: str) -> str:
    """
    Generate human-like explanation with examples using Gemini
    """
    try:
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        full_prompt = f"""
        {prompt}. 
        
        Content to explain:
        {text[:4000]}  # Limit text to avoid token limits
        
        Please provide:
        1. A clear explanation in simple terms
        2. 2-3 practical real-world examples
        3. A summary of key points
        
        Format the response in a natural, conversational way as if you're teaching someone.
        """
        
        response = model.generate_content(full_prompt)
        return response.text
    
    except Exception as e:
        raise Exception(f"Error generating explanation: {str(e)}")