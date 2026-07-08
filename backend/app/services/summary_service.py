from app.services.gemini_client import GeminiClient

class SummaryService:
    def __init__(self, gemini: GeminiClient) -> None:
        self.gemini = gemini

    async def summarize(self, title: str, content: str) -> str:
        fallback = content[:220]
        prompt = f"Use only this journal. Generate a concise 1-2 sentence summary.\nTitle: {title}\nContent: {content}"
        return await self.gemini.generate_text(prompt, fallback)
