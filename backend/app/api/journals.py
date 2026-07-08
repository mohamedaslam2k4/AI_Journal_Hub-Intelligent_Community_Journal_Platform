from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies import current_user
from app.db.mongodb import get_database
from app.models.schemas import JournalCreate, JournalUpdate, SearchRequest
from app.services.ai_service import AIService
from app.services.journal_service import JournalService

router = APIRouter(prefix="/journals", tags=["journals"])

def serialize(j):
    j["id"] = str(j.pop("_id")); return j

@router.get("/public")
async def public_journals():
    docs = await get_database().journals.find({"visibility":"public", "moderation_status":"approved"}).sort("created_at", -1).to_list(50)
    return [serialize(d) for d in docs]

@router.get("/mine")
async def my_journals(user=Depends(current_user)):
    docs = await get_database().journals.find({"author_id": str(user["_id"])}).sort("created_at", -1).to_list(100)
    return [serialize(d) for d in docs]

@router.post("")
async def create_journal(payload: JournalCreate, user=Depends(current_user)):
    return serialize(await JournalService().create(user, payload))

@router.put("/{journal_id}")
async def update_journal(journal_id: str, payload: JournalUpdate, user=Depends(current_user)):
    return serialize(await JournalService().update(journal_id, user, payload))

@router.delete("/{journal_id}")
async def delete_journal(journal_id: str, user=Depends(current_user)):
    deleted = await JournalService().repo.delete(journal_id, str(user["_id"]))
    if not deleted: raise HTTPException(404, "Journal not found")
    return {"deleted": True}

@router.post("/community-search")
async def community_search(payload: SearchRequest, user=Depends(current_user)):
    db = get_database(); ai = AIService(); query_embedding = await ai.embed(payload.query)
    pipeline = [{"$vectorSearch": {"index": "journal_embedding_index", "path": "embedding", "queryVector": query_embedding, "numCandidates": 100, "limit": payload.top_k, "filter": {"visibility": "public", "moderation_status": "approved"}}}]
    hits = await db.embeddings.aggregate(pipeline).to_list(payload.top_k)
    ids = [ObjectId(h["journal_id"]) for h in hits]
    journals = await db.journals.find({"_id": {"$in": ids}}).to_list(payload.top_k)
    summary = await ai.community_summary(payload.query, journals)
    return {"summary": summary, "related_journals": [serialize(j) for j in journals]}
