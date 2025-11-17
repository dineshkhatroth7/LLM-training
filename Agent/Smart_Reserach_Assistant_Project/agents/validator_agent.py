# validator_agent.py
import re

class ValidatorAgent:
    def run(self, state):
        raise NotImplementedError("ValidatorAgent is async-only")

    async def arun(self, state):
        report = getattr(state, "report_markdown", "")
        headers = [h.strip() for h in re.findall(r'#+\s*(.+)', report)]
        required_sections = ["Introduction", "Key Insights", "Future Directions"]
        state.is_valid = all(section in headers for section in required_sections)
        print(f"[ValidatorAgent] Report valid: {state.is_valid}")
        return state
