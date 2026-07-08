from app.services.gemini_client import GeminiClient

class TagService:
    def __init__(self, gemini: GeminiClient) -> None:
        self.gemini = gemini

    async def generate(self, title: str, content: str, category: str) -> list[str]:
        prompt = f"Return JSON only: {{\"tags\": [3 to 8 short relevant tags]}}. Use only this journal. Category: {category}\nTitle: {title}\nContent: {content}"
        result = await self.gemini.generate_json(prompt, {"tags": [category, "Journal"]})
        tags = result.get("tags", [])
        return [str(tag).strip()[:32] for tag in tags if str(tag).strip()][:8] or [category]
