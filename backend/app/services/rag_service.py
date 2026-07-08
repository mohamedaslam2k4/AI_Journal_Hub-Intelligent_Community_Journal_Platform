from app.services.gemini_client import GeminiClient

RAG_POLICY = """
You are AI Journal Hub's Gemini RAG service. Never use Google Search, internet, external websites, or general external knowledge.
Answer only from retrieved community journals below. If the retrieved journals do not contain enough information, respond exactly:
I couldn't find enough information in the community journals.
"""

class RAGService:
    def __init__(self, gemini: GeminiClient) -> None:
        self.gemini = gemini

    async def community_summary(self, query: str, journals: list[dict]) -> str:
        if not journals:
            return "I couldn't find enough information in the community journals."
        context = "\n\n".join(
            f"Journal {idx + 1}\nTitle: {journal['title']}\nSummary: {journal.get('summary', '')}\nContent: {journal.get('content', '')[:1200]}"
            for idx, journal in enumerate(journals)
        )
        fallback = f"Based on {len(journals)} community journals, community members discussed: " + ", ".join(sorted({j.get("category", "Other") for j in journals}))
        prompt = f"{RAG_POLICY}\nQuestion: {query}\nRetrieved Journals:\n{context}"
        return await self.gemini.generate_text(prompt, fallback)
