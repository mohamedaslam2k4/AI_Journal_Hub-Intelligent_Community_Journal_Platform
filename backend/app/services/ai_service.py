from app.services.category_service import CategoryService
from app.services.embedding_service import EmbeddingService
from app.services.gemini_client import GeminiClient
from app.services.moderation_service import ModerationService
from app.services.rag_service import RAGService
from app.services.sentiment_service import SentimentService
from app.services.summary_service import SummaryService
from app.services.tag_service import TagService

class AIService:
    def __init__(self) -> None:
        self.gemini = GeminiClient()
        self.moderation = ModerationService(self.gemini)
        self.summary = SummaryService(self.gemini)
        self.category = CategoryService(self.gemini)
        self.tags = TagService(self.gemini)
        self.sentiment = SentimentService(self.gemini)
        self.embedding = EmbeddingService(self.gemini)
        self.rag = RAGService(self.gemini)

    async def analyze_journal(self, title: str, content: str, visibility: str) -> dict:
        moderation = await self.moderation.moderate(title, content, visibility)
        summary = await self.summary.summarize(title, content)
        category = await self.category.detect(title, content)
        tags = await self.tags.generate(title, content, category)
        sentiment = await self.sentiment.analyze(title, content)
        embedding = await self.embedding.embed_journal(title, content, summary)
        return {**moderation, **sentiment, "category": category, "tags": tags, "summary": summary, "embedding": embedding}

    async def embed(self, text: str) -> list[float]:
        return await self.embedding.embed_query(text)

    async def community_summary(self, query: str, journals: list[dict]) -> str:
        return await self.rag.community_summary(query, journals)
