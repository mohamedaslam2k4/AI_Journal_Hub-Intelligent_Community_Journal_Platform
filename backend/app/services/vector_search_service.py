from bson import ObjectId
from app.core.config import get_settings
from app.db.mongodb import get_database
from app.services.embedding_service import EmbeddingService

class VectorSearchService:
    def __init__(self, embedding_service: EmbeddingService) -> None:
        self.embedding_service = embedding_service
        self.settings = get_settings()

    async def search_public_journals(self, query: str, top_k: int) -> list[dict]:
        db = get_database()
        query_embedding = await self.embedding_service.embed_query(query)
        pipeline = [
            {
                "$vectorSearch": {
                    "index": self.settings.vector_index_name,
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": max(top_k * 10, 100),
                    "limit": top_k,
                    "filter": {"visibility": "public", "moderation_status": "approved"},
                }
            },
            {"$project": {"embedding": 0, "score": {"$meta": "vectorSearchScore"}}},
        ]
        journals = await db.journals.aggregate(pipeline).to_list(top_k)
        for journal in journals:
            journal["id"] = str(journal.pop("_id")) if isinstance(journal.get("_id"), ObjectId) else journal.get("id")
        return journals
