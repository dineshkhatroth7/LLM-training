import os
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="AI API with Gemini", version="1.0.0")

# -------- Request Models -------- #
class TextInput(BaseModel):
    text: str

# -------- Endpoints -------- #

@app.post("/v1/summarize")
def summarize_text(input_data: TextInput):
    """
    Summarize the given paragraph using Gemini
    """
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    prompt = f"Summarize the following text in 3-4 sentences:\n\n{input_data.text}"
    
    response = model.generate_content(prompt)
    return {"summary": response.text.strip()}


@app.post("/v1/extract/entities")
def extract_entities(input_data: TextInput):
    """
    Extract entities from medical text (drug names, diseases, companies, dates, etc.)
    """
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    prompt = f"""
    Extract named entities from the following text.
    Return them as JSON with keys: drugs, diseases, companies, products, dates, others.

    Text: {input_data.text}
    """
    
    response = model.generate_content(prompt)
    return {"entities": response.text.strip()}
