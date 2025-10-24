import gradio as gr
from google import genai
import os

# Load Gemini API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("Please set GEMINI_API_KEY or GOOGLE_API_KEY in environment variables.")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

# Define chatbot function
def chat_with_gemini(message, history):
    """
    message: latest user message
    history: list of (user, bot) message tuples
    """
    # Build full conversation context
    context = ""
    for user_msg, bot_msg in history:
        context += f"User: {user_msg}\nAssistant: {bot_msg}\n"
    context += f"User: {message}\nAssistant:"

    # Send to Gemini model
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=context
    )
    reply = response.text.strip()
    return reply

# Gradio UI
with gr.Blocks(title="Gemini Chatbot") as demo:
    gr.Markdown("## 💬 Gemini Chatbot\nAsk anything!")
    chatbot = gr.Chatbot(height=400)
    msg = gr.Textbox(placeholder="Type your message here...")
    clear = gr.Button("Clear Chat")

    def respond(message, chat_history):
        reply = chat_with_gemini(message, chat_history)
        chat_history.append((message, reply))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch()
