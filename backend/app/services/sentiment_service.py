from app.services.gemini_client import GeminiClient

SENTIMENTS = {"Positive", "Neutral", "Negative"}
EMOTIONS = {"Happy", "Sad", "Excited", "Motivated", "Confident", "Anxious", "Frustrated", "Grateful"}

class SentimentService:
    def __init__(self, gemini: GeminiClient) -> None:
        self.gemini = gemini

    async def analyze(self, title: str, content: str) -> dict:
        prompt = "Return JSON only: {\"sentiment\": \"Positive|Neutral|Negative\", \"emotion\": \"Happy|Sad|Excited|Motivated|Confident|Anxious|Frustrated|Grateful\"}. Sentiment never affects moderation.\n" f"Title: {title}\nContent: {content}"
        result = await self.gemini.generate_json(prompt, {"sentiment": "Neutral", "emotion": "Motivated"})
        sentiment = result.get("sentiment", "Neutral")
        emotion = result.get("emotion", "Motivated")
        return {"sentiment": sentiment if sentiment in SENTIMENTS else "Neutral", "emotion": emotion if emotion in EMOTIONS else "Motivated"}
