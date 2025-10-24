import gradio as gr
import requests

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/chat"

def chat_with_backend(message, history):
    payload = {
        "message": message,
        "history": history
    }
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["reply"]
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Define Gradio interface
with gr.Blocks(title="Gemini Chatbot") as demo:
    gr.Markdown("## 💬 Gemini Chatbot — powered by FastAPI backend")
    chatbot = gr.Chatbot(height=450)
    msg = gr.Textbox(placeholder="Type your message here...", label="Message")
    clear = gr.Button("Clear Chat")

    def respond(message, chat_history):
        reply = chat_with_backend(message, chat_history)
        chat_history.append((message, reply))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch()
