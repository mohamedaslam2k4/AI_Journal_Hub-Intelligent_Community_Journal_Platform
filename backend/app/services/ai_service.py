import json
from openai import AsyncOpenAI
from app.core.config import get_settings

SYSTEM_POLICY = """You are the AI pipeline for AI Journal Hub. Never browse, cite, or use internet knowledge. For RAG answers, use only provided journal excerpts. Moderation rejects only hate, profanity, threats, violence, self-harm encouragement, explicit sexual content, illegal activity, spam, or phishing. Negative emotions and failures are safe personal experiences."""

class AIService:
    def __init__(self) -> None:
        settings = get_settings()
        self.settings = settings
        self.client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    async def analyze_journal(self, title: str, content: str, visibility: str) -> dict:
        if not self.client:
            return self._fallback_analysis(title, content, visibility)
        prompt = f"""Analyze this journal as strict JSON with keys: moderation_status, moderation_reason, sentiment, emotion, category, tags, summary. Visibility={visibility}. Categories: Career, Programming, Education, Health, Travel, Finance, Relationships, Fitness, Personal Growth, Business, Other. Title: {title}\nContent: {content}"""
        response = await self.client.chat.completions.create(
            model=self.settings.openai_chat_model,
            messages=[{"role": "system", "content": SYSTEM_POLICY}, {"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        data = json.loads(response.choices[0].message.content or "{}")
        if visibility == "private":
            data["moderation_status"] = "private"
        return data

    async def embed(self, text: str) -> list[float]:
        if not self.client:
            return [0.0] * self.settings.embedding_dimension
        result = await self.client.embeddings.create(model=self.settings.openai_embedding_model, input=text)
        return result.data[0].embedding

    async def community_summary(self, query: str, journals: list[dict]) -> str:
        if not journals:
            return "I couldn't find enough information in the community journals."
        if not self.client:
            return f"Based on {len(journals)} community journals, users frequently discussed: " + ", ".join(sorted({j.get("category", "Other") for j in journals}))
        context = "\n\n".join(f"Title: {j['title']}\nSummary: {j.get('summary','')}\nContent: {j.get('content','')[:1200]}" for j in journals)
        prompt = f"Query: {query}\nUse only these retrieved journals. If insufficient, answer exactly: I couldn't find enough information in the community journals.\n\n{context}"
        response = await self.client.chat.completions.create(
            model=self.settings.openai_chat_model,
            messages=[{"role": "system", "content": SYSTEM_POLICY}, {"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content or "I couldn't find enough information in the community journals."

    def _fallback_analysis(self, title: str, content: str, visibility: str) -> dict:
        lowered = f"{title} {content}".lower()
        category = "Programming" if any(x in lowered for x in ["python", "react", "code", "fastapi"]) else "Career" if "interview" in lowered else "Other"
        return {"moderation_status": "private" if visibility == "private" else "approved", "moderation_reason": None, "sentiment": "Neutral", "emotion": "Motivated", "category": category, "tags": [category, "Journal"], "summary": content[:220]}
