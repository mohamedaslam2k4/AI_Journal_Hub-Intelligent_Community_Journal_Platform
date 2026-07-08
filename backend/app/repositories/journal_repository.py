from datetime import datetime, timezone
from bson import ObjectId
from app.db.mongodb import get_database

class JournalRepository:
    @property
    def db(self):
        return get_database()

    async def create(self, document: dict) -> dict:
        now = datetime.now(timezone.utc)
        document.update({"created_at": now, "updated_at": now})
        result = await self.db.journals.insert_one(document)
        document["_id"] = result.inserted_id
        return document

    async def update(self, journal_id: str, owner_id: str, fields: dict) -> dict | None:
        fields["updated_at"] = datetime.now(timezone.utc)
        await self.db.journals.update_one({"_id": ObjectId(journal_id), "author_id": owner_id}, {"$set": fields})
        return await self.db.journals.find_one({"_id": ObjectId(journal_id), "author_id": owner_id})

    async def delete(self, journal_id: str, owner_id: str) -> int:
        result = await self.db.journals.delete_one({"_id": ObjectId(journal_id), "author_id": owner_id})
        await self.db.ai_analysis.delete_one({"journal_id": journal_id})
        return result.deleted_count
