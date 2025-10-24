from langchain_tavily import TavilySearch


api_key = "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"

web_search = TavilySearch(max_results=3, tavily_api_key=api_key)

result = web_search.invoke("who is the mayor of NYC?")
print(result["results"][0]["content"])
