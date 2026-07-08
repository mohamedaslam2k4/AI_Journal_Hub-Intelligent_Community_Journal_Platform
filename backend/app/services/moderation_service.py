from app.services.gemini_client import GeminiClient

MODERATION_POLICY = """
You are AI Journal Hub's Gemini moderation engine. Use no internet, Google Search, external websites, or external knowledge.
Reject ONLY: Hate Speech, Profanity, Violence, Threats, Self-harm encouragement, Illegal activities, Adult explicit content, Spam.
Always allow: failure stories, interview rejection, stress, depression discussion without encouragement, career problems, life struggles, personal experiences, and negative emotions.
Return JSON only: {"moderation_status":"approved"|"rejected"|"private", "moderation_reason": string|null}
"""

class ModerationService:
    def __init__(self, gemini: GeminiClient) -> None:
        self.gemini = gemini

    async def moderate(self, title: str, content: str, visibility: str) -> dict:
        if visibility == "private":
            return {"moderation_status": "private", "moderation_reason": None}
        fallback = {"moderation_status": "approved", "moderation_reason": None}
        prompt = f"{MODERATION_POLICY}\nTitle: {title}\nContent: {content}"
        result = await self.gemini.generate_json(prompt, fallback)
        status = result.get("moderation_status")
        if status not in {"approved", "rejected"}:
            return fallback
        return {"moderation_status": status, "moderation_reason": result.get("moderation_reason")}
