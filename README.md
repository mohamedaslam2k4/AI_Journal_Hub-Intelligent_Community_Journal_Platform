# AI Journal Hub – Intelligent Community Journal Platform

AI Journal Hub is a production-oriented full-stack portfolio project for building a community journal platform with AI moderation, analytics, semantic search, and retrieval-augmented generation (RAG). The application is intentionally designed so AI answers are grounded only in journals stored in MongoDB Atlas Vector Search—never internet search or external websites.

## Architecture

```text
backend/
  app/
    api/              FastAPI route modules
    core/             config, security, JWT, errors
    db/               MongoDB connection and indexes
    models/           Pydantic schemas and domain models
    repositories/     MongoDB data access layer
    services/         auth, journals, AI pipeline, vector search, analytics
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
- AI journal processing pipeline: moderation, sentiment, emotion, category, tags, summary, and embeddings.
- Strict RAG community search that passes only retrieved journal context to the LLM.
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

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## MongoDB Atlas Vector Search Index

Create a vector search index on the `embeddings` collection. The default embedding dimension is configured by `EMBEDDING_DIMENSION`.

```json
{
  "fields": [
    { "type": "vector", "path": "embedding", "numDimensions": 1536, "similarity": "cosine" },
    { "type": "filter", "path": "visibility" },
    { "type": "filter", "path": "moderation_status" }
  ]
}
```

## Development Roadmap

1. Configure environment variables and MongoDB Atlas credentials.
2. Start the FastAPI backend and confirm `/health` returns `ok`.
3. Register a user, scan the generated QR code in Google Authenticator, and verify OTP.
4. Create private and public journals; public journals pass through AI moderation before appearing publicly.
5. Run AI Community Search to retrieve similar journals and generate a grounded community summary.
6. Deploy the backend to Render/Fly.io and frontend to Vercel/Netlify.

## Resume Description

Built an AI-powered community journaling platform using React, FastAPI, MongoDB Atlas, JWT, TOTP 2FA, and MongoDB Atlas Vector Search. Implemented a safe AI pipeline for moderation, sentiment analytics, automatic categorization, tagging, summarization, embeddings, semantic search, and RAG responses grounded exclusively in stored community journals.
