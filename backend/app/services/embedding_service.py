from app.services.gemini_client import GeminiClient

class EmbeddingService:
    def __init__(self, gemini: GeminiClient) -> None:
        self.gemini = gemini

    async def embed_journal(self, title: str, content: str, summary: str) -> list[float]:
        return await self.gemini.embed(f"Title: {title}\nSummary: {summary}\nContent: {content}")

    async def embed_query(self, query: str) -> list[float]:
        return await self.gemini.embed(query)
