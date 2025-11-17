import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class GeminiClient:
    def __init__(self, model_name="models/gemini-2.5-flash"): 
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(model_name)

    async def generate(self, prompt: str) -> str:
        loop = asyncio.get_running_loop()
        try:
            response = await loop.run_in_executor(None, self.model.generate_content, prompt)
            return response.text.strip()
        except Exception as e:
            print(f"[GeminiClient] LLM generation failed: {e}")
            return "LLM generation failed."
