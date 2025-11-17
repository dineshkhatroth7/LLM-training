# analysis_agent.py
from collections import Counter
from textblob import TextBlob
import asyncio

class AnalysisAgent:
    def run(self, state):
        documents = getattr(state, "documents", [])
        text = " ".join(documents).lower()

        top_keywords = Counter(text.split()).most_common(5)
        sentiment_score = TextBlob(text).sentiment.polarity
        sentiment = "Positive" if sentiment_score >= 0 else "Negative"
        themes = ["automation", "efficiency", "ethics"]  # placeholder

        state.analysis = {
            "query": getattr(state, "query", ""),
            "top_keywords": top_keywords,
            "sentiment": sentiment,
            "themes": themes
        }
        print(f"[AnalysisAgent] Top keywords: {state.analysis['top_keywords']}, Sentiment: {state.analysis['sentiment']}")
        return state

    async def arun(self, state):
        await asyncio.sleep(0.1)
        return self.run(state)
