from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies import current_user
from app.db.mongodb import get_database
from app.models.schemas import JournalCreate, JournalUpdate, SearchRequest
from app.services.ai_service import AIService
from app.services.embedding_service import EmbeddingService
from app.services.gemini_client import GeminiClient
from app.services.journal_service import JournalService
from app.services.vector_search_service import VectorSearchService

router = APIRouter(prefix="/journals", tags=["journals"])

def serialize(journal: dict) -> dict:
    journal["id"] = str(journal.pop("_id"))
    journal.pop("embedding", None)
    return journal

@router.get("/public")
async def public_journals():
    docs = await get_database().journals.find({"visibility": "public", "moderation_status": "approved"}, {"embedding": 0}).sort("created_at", -1).to_list(50)
    return [serialize(doc) for doc in docs]

@router.get("/mine")
async def my_journals(user=Depends(current_user)):
    docs = await get_database().journals.find({"author_id": str(user["_id"])}, {"embedding": 0}).sort("created_at", -1).to_list(100)
    return [serialize(doc) for doc in docs]

@router.post("")
async def create_journal(payload: JournalCreate, user=Depends(current_user)):
    return serialize(await JournalService().create(user, payload))

@router.put("/{journal_id}")
async def update_journal(journal_id: str, payload: JournalUpdate, user=Depends(current_user)):
    return serialize(await JournalService().update(journal_id, user, payload))

@router.delete("/{journal_id}")
async def delete_journal(journal_id: str, user=Depends(current_user)):
    deleted = await JournalService().repo.delete(journal_id, str(user["_id"]))
    if not deleted:
        raise HTTPException(404, "Journal not found")
    return {"deleted": True}

@router.post("/community-search")
async def community_search(payload: SearchRequest, user=Depends(current_user)):
    gemini = GeminiClient()
    vector_search = VectorSearchService(EmbeddingService(gemini))
    journals = await vector_search.search_public_journals(payload.query, payload.top_k)
    summary = await AIService().community_summary(payload.query, journals)
    return {"summary": summary, "related_journals": journals}
