from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import analytics, auth, journals
from app.db.mongodb import close_mongo, connect_to_mongo

app = FastAPI(title="AI Journal Hub API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth.router, prefix="/api")
app.include_router(journals.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")

@app.on_event("startup")
async def startup():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown():
    await close_mongo()

@app.get("/health")
def health():
    return {"status": "ok"}
