from langchain_tavily import TavilySearch
import re

# Research Agent
def research_agent(query: str) -> str:
    web_search = TavilySearch(max_results=3, tavily_api_key="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")
    results = web_search.invoke(query)
    return results["results"][0]["content"]

# Math Agent with simple parser
def math_agent(query: str) -> str:
    query = query.lower()
    
    add_match = re.search(r"add (\d+) and (\d+)", query)
    if add_match:
        x, y = int(add_match.group(1)), int(add_match.group(2))
        return str(x + y)
    
    mul_match = re.search(r"multiply (\d+) and (\d+)", query)
    if mul_match:
        x, y = int(mul_match.group(1)), int(mul_match.group(2))
        return str(x * y)
    
    div_match = re.search(r"divide (\d+) by (\d+)", query)
    if div_match:
        x, y = int(div_match.group(1)), int(div_match.group(2))
        return str(x / y)
    
    # Custom pattern: "add N to M"
    add_to_match = re.search(r"add (\d+) to (\d+)", query)
    if add_to_match:
        x, y = int(add_to_match.group(1)), int(add_to_match.group(2))
        return str(x + y)
    
    return "Could not parse math query"

# Workflow Agent
def agent_workflow(query: str) -> str:
    query_lower = query.lower()
    
    # Check if query contains "add", "multiply", "divide"
    if "add" in query_lower or "multiply" in query_lower or "divide" in query_lower:
        # Handle mixed query: mayor + math
        if "mayor" in query_lower and "number of letters in their first name" in query_lower:
            research_result = research_agent("Who is the current mayor of NYC?")
            # Extract first name (assume 4th word from result text, may need refinement)
            first_name = research_result.split()[3]
            num_letters = len(first_name)
            # Replace English phrase with number
            math_query = query_lower.replace("number of letters in their first name", str(num_letters))
            return math_agent(math_query)
        else:
            return math_agent(query_lower)
    else:
        return research_agent(query)

# -------------------------
# Test Queries
# -------------------------
query1 = "Who is the current mayor of New York City?"
print("Research Result:", agent_workflow(query1))

query2 = "Add 45 and 78"
print("Math Result:", agent_workflow(query2))

query3 = "Find the current mayor of NYC and add 5 to the number of letters in their first name"
print("Mixed Result:", agent_workflow(query3))
