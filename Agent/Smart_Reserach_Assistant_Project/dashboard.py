import gradio as gr
import httpx
import asyncio

API_URL = "http://127.0.0.1:8000/run"

async def fetch_report(query: str):
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(API_URL, json={"query": query})
            response.raise_for_status()
            return response.json()
        except httpx.ReadTimeout:
            return {"error": "Backend took too long to respond."}
        except Exception as e:
            return {"error": str(e)}

def run_query(query: str):
    if not query.strip():
        return "Please enter a topic", "<p>No HTML output</p>"

    # Use asyncio.run in a **new event loop** safely
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(fetch_report(query))
    loop.close()

    if "error" in result:
        return result["error"], "<p>No HTML output</p>"

    markdown_report = result.get("report_markdown", "_No report generated._")
    html_report = result.get("report_html", "<p>No HTML output</p>")
    is_valid = " Valid" if result.get("is_valid", False) else "Invalid"

    return markdown_report, html_report, is_valid

# Build Gradio interface
with gr.Blocks(title="Smart Research Assistant") as demo:
    gr.Markdown("# Smart Research Assistant")
    gr.Markdown("Enter a topic and let AI agents generate a report.")

    with gr.Row():
        query_input = gr.Textbox(label="Enter research topic", placeholder="e.g., Artificial Intelligence")
        run_button = gr.Button("Run Research")

    with gr.Tabs():
        with gr.TabItem("Markdown Report"):
            markdown_output = gr.Markdown()
        with gr.TabItem("HTML View"):
            html_output = gr.HTML()
        with gr.TabItem("Validation"):
            validation_output = gr.Textbox(label="Validation Result")

    run_button.click(fn=run_query, inputs=query_input, outputs=[markdown_output, html_output, validation_output])

demo.launch()
