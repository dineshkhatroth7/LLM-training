from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
import os


API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Please set GEMINI_API_KEY in environment variables.")


client = genai.Client(api_key=API_KEY)



app = FastAPI(title="Gemini Chatbot API")

class ChatRequest(BaseModel):
    message: str
    history: list[tuple[str, str]] = []

class ChatResponse(BaseModel):
    reply: str
    history: list[tuple[str, str]]


def generate_reply(message: str, history: list[tuple[str, str]]):
    context = ""
    for user_msg, bot_msg in history:
        context += f"User: {user_msg}\nAssistant: {bot_msg}\n"
    context += f"User: {message}\nAssistant:"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=context
    )
    return response.text.strip()


@app.post("/chat", response_model=ChatResponse)
async def chat_with_gemini(req: ChatRequest):
    try:
        reply = generate_reply(req.message, req.history)
        new_history = req.history + [(req.message, reply)]
        return ChatResponse(reply=reply, history=new_history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Gemini Chatbot API is running "}