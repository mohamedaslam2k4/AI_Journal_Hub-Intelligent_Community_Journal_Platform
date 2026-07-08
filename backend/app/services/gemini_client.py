import json
import logging
from google import genai
from app.core.config import get_settings
from app.core.retry import retry_async

logger = logging.getLogger("ai_journal_hub.gemini")

class GeminiClient:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = genai.Client(api_key=self.settings.gemini_api_key) if self.settings.gemini_api_key else None

    async def generate_json(self, prompt: str, fallback: dict) -> dict:
        if not self.client:
            return fallback

        async def operation():
            return await self.client.aio.models.generate_content(
                model=self.settings.gemini_model,
                contents=prompt,
                config={"response_mime_type": "application/json"},
            )

        response = await retry_async(operation)
        try:
            return json.loads(response.text or "{}")
        except json.JSONDecodeError:
            logger.warning("Gemini returned non-JSON response for JSON prompt")
            return fallback

    async def generate_text(self, prompt: str, fallback: str) -> str:
        if not self.client:
            return fallback

        async def operation():
            return await self.client.aio.models.generate_content(model=self.settings.gemini_model, contents=prompt)

        response = await retry_async(operation)
        return response.text or fallback

    async def embed(self, text: str) -> list[float]:
        if not self.client:
            return [0.0] * 768

        async def operation():
            return await self.client.aio.models.embed_content(model=self.settings.embedding_model, contents=text)

        response = await retry_async(operation)
        return response.embeddings[0].values
