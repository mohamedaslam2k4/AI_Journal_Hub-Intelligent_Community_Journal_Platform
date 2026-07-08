from bson import ObjectId
from fastapi import HTTPException
from app.db.mongodb import get_database
from app.models.schemas import JournalCreate, JournalUpdate
from app.repositories.journal_repository import JournalRepository
from app.services.ai_service import AIService

class JournalService:
    def __init__(self) -> None:
        self.repo = JournalRepository()
        self.ai = AIService()

    async def create(self, user: dict, payload: JournalCreate) -> dict:
        analysis = await self.ai.analyze_journal(payload.title, payload.content, payload.visibility.value)
        doc = {"title": payload.title, "content": payload.content, "visibility": payload.visibility.value, "author_id": str(user["_id"]), "author_name": user["name"], **analysis}
        journal = await self.repo.create(doc)
        await self._persist_ai_artifacts(journal, analysis)
        return journal

    async def update(self, journal_id: str, user: dict, payload: JournalUpdate) -> dict:
        current = await get_database().journals.find_one({"_id": ObjectId(journal_id), "author_id": str(user["_id"])})
        if not current:
            raise HTTPException(404, "Journal not found")
        title = payload.title or current["title"]
        content = payload.content or current["content"]
        visibility = (payload.visibility.value if payload.visibility else current["visibility"])
        analysis = await self.ai.analyze_journal(title, content, visibility)
        fields = {k: v for k, v in {"title": payload.title, "content": payload.content, "visibility": visibility, **analysis}.items() if v is not None}
        journal = await self.repo.update(journal_id, str(user["_id"]), fields)
        await self._persist_ai_artifacts(journal, analysis)
        return journal

    async def _persist_ai_artifacts(self, journal: dict, analysis: dict) -> None:
        db = get_database(); journal_id = str(journal["_id"])
        await db.ai_analysis.update_one({"journal_id": journal_id}, {"$set": {"journal_id": journal_id, **analysis}}, upsert=True)
        if journal.get("moderation_status") in ["approved", "private"]:
            embedding = await self.ai.embed(f"{journal['title']}\n{journal['content']}\n{journal.get('summary','')}")
            await db.embeddings.update_one({"journal_id": journal_id}, {"$set": {"journal_id": journal_id, "embedding": embedding, "visibility": journal["visibility"], "moderation_status": journal["moderation_status"]}}, upsert=True)
