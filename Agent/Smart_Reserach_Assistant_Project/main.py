from fastapi import FastAPI
from pydantic import BaseModel
from langgraph.graph import StateGraph
from state import ResearchState
from utils.llm_client import GeminiClient
from agents.search_agent import SearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.summarizer_agent import SummarizerAgent
from agents.validator_agent import ValidatorAgent
from agents.format_agent import FormatAgent
from langfuse import get_client, observe
import os

# ==================================================
# Environment setup
# ==================================================
# Required env vars: LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_BASE_URL
# Also required: GEMINI_API_KEY for GeminiClient

# ==================================================
# Initialize clients
# ==================================================
llm_client = GeminiClient()
langfuse = get_client()  # Automatically reads keys & base URL

# ==================================================
# Initialize FastAPI
# ==================================================
app = FastAPI(title="Smart Research Assistant")

# ==================================================
# Input model
# ==================================================
class ResearchInput(BaseModel):
    query: str
    max_results: int = 3


# ==================================================
# Helper: traced wrapper for each agent
# ==================================================
@observe(name="search_agent")
async def traced_search_agent(state: ResearchState):
    return await SearchAgent().arun(state)

@observe(name="analysis_agent")
async def traced_analysis_agent(state: ResearchState):
    return await AnalysisAgent().arun(state)

@observe(name="summarizer_agent")
async def traced_summarizer_agent(state: ResearchState):
    return await SummarizerAgent(llm_client).arun(state)

@observe(name="validator_agent")
async def traced_validator_agent(state: ResearchState):
    return await ValidatorAgent().arun(state)

@observe(name="format_agent")
async def traced_format_agent(state: ResearchState):
    return await FormatAgent().arun(state)


# ==================================================
# Build workflow graph
# ==================================================
def build_graph():
    g = StateGraph(ResearchState)

    g.add_node("search_agent", traced_search_agent)
    g.add_node("analysis_agent", traced_analysis_agent)
    g.add_node("summarizer_agent", traced_summarizer_agent)
    g.add_node("validator_agent", traced_validator_agent)
    g.add_node("format_agent", traced_format_agent)

    g.set_entry_point("search_agent")
    g.add_edge("search_agent", "analysis_agent")
    g.add_edge("analysis_agent", "summarizer_agent")
    g.add_edge("summarizer_agent", "validator_agent")
    g.add_edge("validator_agent", "format_agent")

    return g.compile()


graph = build_graph()

# ==================================================
# API Endpoint (Workflow-level trace)
# ==================================================
@app.post("/run")
@observe(name="research_workflow")  # Top-level trace
async def run_workflow(input: ResearchInput):
    try:
        # Create initial state
        initial_state = ResearchState(query=input.query, max_results=input.max_results)

        # Run the workflow graph
        result_state = await graph.ainvoke(initial_state)

        # Return the result
        return result_state.dict() if not isinstance(result_state, dict) else result_state

    except Exception as e:
        return {"error": str(e)}
