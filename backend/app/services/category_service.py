from app.services.gemini_client import GeminiClient

CATEGORIES = {"Career", "Programming", "Education", "Health", "Business", "Finance", "Travel", "Fitness", "Relationships", "Personal Growth", "Other"}

class CategoryService:
    def __init__(self, gemini: GeminiClient) -> None:
        self.gemini = gemini

    async def detect(self, title: str, content: str) -> str:
        fallback = "Programming" if any(x in f"{title} {content}".lower() for x in ["python", "react", "mongodb", "fastapi", "code"]) else "Other"
        prompt = "Return JSON only: {\"category\": one of Career, Programming, Education, Health, Business, Finance, Travel, Fitness, Relationships, Personal Growth, Other}.\n" f"Title: {title}\nContent: {content}"
        result = await self.gemini.generate_json(prompt, {"category": fallback})
        category = result.get("category", fallback)
        return category if category in CATEGORIES else fallback
