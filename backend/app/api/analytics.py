from fastapi import APIRouter
from app.db.mongodb import get_database

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/community")
async def community_analytics():
    db = get_database(); public_filter = {"visibility":"public", "moderation_status":"approved"}
    total_public = await db.journals.count_documents(public_filter); total_users = await db.users.count_documents({})
    sentiment = await db.journals.aggregate([{"$match": public_filter}, {"$group": {"_id":"$sentiment", "count":{"$sum":1}}}]).to_list(10)
    categories = await db.journals.aggregate([{"$match": public_filter}, {"$group": {"_id":"$category", "count":{"$sum":1}}}, {"$sort":{"count":-1}}]).to_list(10)
    tags = await db.journals.aggregate([{"$match": public_filter}, {"$unwind":"$tags"}, {"$group": {"_id":"$tags", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":15}]).to_list(15)
    recent = await db.journals.find(public_filter, {"title":1,"author_name":1,"created_at":1}).sort("created_at", -1).to_list(10)
    for r in recent: r["id"] = str(r.pop("_id"))
    return {"total_public_journals": total_public, "total_users": total_users, "sentiment": sentiment, "popular_categories": categories, "popular_tags": tags, "recent_activity": recent}
