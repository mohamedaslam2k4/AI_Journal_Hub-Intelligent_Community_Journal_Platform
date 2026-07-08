# AI Journal Hub – Intelligent Community Journal Platform

AI Journal Hub is a production-oriented full-stack portfolio project for a community journal platform with Google Gemini-powered moderation, analytics, semantic search, and retrieval-augmented generation (RAG). The AI layer is intentionally grounded only in journals stored in MongoDB Atlas Vector Search. It does not use Google Search, internet search, external websites, or external knowledge for community answers.

## Architecture

```text
backend/
  app/
    api/              FastAPI route modules
    core/             config, security, centralized errors, retry, rate limiting
    db/               MongoDB connection and indexes
    models/           Pydantic schemas and domain models
    repositories/     MongoDB data access layer
    services/         Gemini, moderation, summary, category, tags, sentiment, embeddings, RAG, vector search
frontend/
  src/
    api/              Axios client
    components/       shared UI components
    pages/            route-level screens
    routes/           React Router setup
    state/            auth context
    styles/           Tailwind entry
```

## Key Features

- JWT authentication with Google Authenticator-compatible TOTP two-factor authentication.
- Google Gemini 2.5 Flash for moderation, summarization, category detection, tags, sentiment, emotion, community summaries, RAG answers, and general AI chat capabilities.
- Google `text-embedding-004` embeddings stored directly on journal documents.
- MongoDB Atlas Vector Search over the `journals.embedding` field.
- Strict RAG community search that passes only retrieved journal context to Gemini.
- Public journals show only approved public content; private journals remain owner-only.
- Analytics dashboard with community sentiment, category distribution, popular tags, totals, and recent activity.
- React + Tailwind UI with responsive cards, dark mode styling, and modular pages.

## Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Environment Variables

```env
APP_NAME="AI Journal Hub"
ENVIRONMENT=development
JWT_SECRET=change-me
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
MONGODB_URI=
MONGODB_DB=ai_journal_hub
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash
EMBEDDING_MODEL=text-embedding-004
VECTOR_INDEX_NAME=journal_embedding_index
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## MongoDB Atlas Vector Search Index

Create a vector search index named `journal_embedding_index` on the `journals` collection. Google `text-embedding-004` returns 768-dimensional vectors.

```json
{
  "fields": [
    { "type": "vector", "path": "embedding", "numDimensions": 768, "similarity": "cosine" },
    { "type": "filter", "path": "visibility" },
    { "type": "filter", "path": "moderation_status" }
  ]
}
```

## Gemini AI Pipeline

1. The user creates or updates a journal.
2. Gemini moderation rejects only unsafe public content: hate speech, profanity, violence, threats, self-harm encouragement, illegal activities, adult explicit content, or spam.
3. Gemini generates sentiment, emotion, category, tags, and summary.
4. Google Embedding API generates a journal embedding.
5. The journal document is saved in MongoDB with the embedding field.
6. Approved public journals become searchable through MongoDB Atlas Vector Search.

## RAG Workflow

1. User submits a community question.
2. Google Embedding API converts the question to a vector.
3. MongoDB Atlas Vector Search retrieves the top matching approved public journals.
4. Gemini receives only those retrieved journals as context.
5. If the retrieved journals are insufficient, Gemini must answer: `I couldn't find enough information in the community journals.`

## Development Roadmap

1. Configure environment variables and MongoDB Atlas credentials.
2. Start the FastAPI backend and confirm `/health` returns `ok`.
3. Register a user, scan the generated QR code in Google Authenticator, and verify OTP.
4. Create private and public journals; public journals pass through Gemini moderation before appearing publicly.
5. Run AI Community Search to retrieve similar journals and generate a grounded Gemini community summary.
6. Deploy the backend to Render and frontend to Vercel.

## Resume Description

Built an AI-powered community journaling platform using React, FastAPI, MongoDB Atlas, JWT, TOTP 2FA, Google Gemini 2.5 Flash, Google embeddings, and MongoDB Atlas Vector Search. Implemented a safe AI pipeline for moderation, sentiment analytics, emotion detection, automatic categorization, tagging, summarization, embeddings, semantic search, and RAG responses grounded exclusively in stored community journals.
