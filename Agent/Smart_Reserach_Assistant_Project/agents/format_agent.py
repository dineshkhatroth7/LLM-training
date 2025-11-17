#format_agent.py
import markdown

class FormatAgent:
    def run(self, state):
        raise NotImplementedError("FormatAgent is async-only")

    async def arun(self, state):
        report_md = getattr(state, "report_markdown", "")
        state.report_html = markdown.markdown(report_md)
        print(f"[FormatAgent] Converted report to HTML, length: {len(state.report_html)}")
        return state
