# summarizer_agent.py
class SummarizerAgent:
    def __init__(self, llm_client):
        self.llm = llm_client

    def run(self, state):
        raise NotImplementedError("Sync mode not supported for async LLM client")

    async def arun(self, state):
        query = getattr(state, "query", "")
        documents = getattr(state, "documents", [])
        analysis = getattr(state, "analysis", {})

        prompt = f"""
You are a Smart Research Summarizer Agent.
Write a professional research report on: "{query}".

Reference documents:
{documents}

Analysis results:
{analysis}

Create a Markdown report with:
- Introduction
- Key Insights
- Trends and Sentiment
- Future Directions
- Conclusion
"""
        report = await self.llm.generate(prompt)
        state.report_markdown = report
        print(f"[SummarizerAgent] Generated report ({len(report)} characters)")
        return state
