# state.py
from pydantic import BaseModel
from typing import List, Dict, Any

class ResearchState(BaseModel):
    query: str = ""
    max_results: int = 3
    documents: List[str] = []
    analysis: Dict[str, Any] = {}
    report_markdown: str = ""
    report_html: str = ""
    is_valid: bool = False
