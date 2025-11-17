# search_agent.py
import random
import asyncio

class SearchAgent:
    def _run_sync(self, state):
        query = getattr(state, "query", "")
        max_results = getattr(state, "max_results", 3)

        mock_data = [
            f"Research paper on {query} and its applications in 2023",
            f"Trends of {query} adoption in industry",
            f"Recent advancements in {query} algorithms",
            f"Limitations and ethics of {query} usage"
        ]

        results = random.sample(mock_data, min(max_results, len(mock_data)))
        state.documents = results
        print(f"[SearchAgent] Retrieved {len(results)} documents")
        return state

    async def _run_async(self, state):
        await asyncio.sleep(0)
        return self._run_sync(state)

    def run(self, state):
        return self._run_sync(state)

    async def arun(self, state):
        return await self._run_async(state)
