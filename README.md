# AI CRM — HCP Interaction Logger

A full-stack AI-powered CRM tool for pharmaceutical field reps to log Healthcare Professional (HCP) interactions via natural language chat. Describe a visit in plain English; the AI extracts structured data, auto-populates a form, and saves the record to PostgreSQL — all in real time via streaming.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Environment Variables](#environment-variables)
- [API Overview](#api-overview)
- [Database Schema](#database-schema)
- [Deployment](#deployment)

---

## Overview

Field reps describe an HCP interaction in plain English:

> *"Called Dr. Lisa Park today at 10am, discussed Neurology drug Z efficacy, she seemed neutral, scheduled a follow-up for next week"*

The AI assistant:
1. Parses the message and extracts all structured fields (HCP, type, date, time, topics, sentiment, etc.)
2. Pre-fills the form panel in real time as it streams the response
3. Shows a confirmation summary — no data is saved until the rep confirms
4. Saves the record to the database on confirmation
5. Generates 3 contextual follow-up action suggestions

Reps can also retrieve past interactions, edit existing records via chat, or use voice input (Groq Whisper transcription).

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                          Browser                             │
│                                                              │
│  ┌───────────────────────┐    ┌───────────────────────────┐  │
│  │      Form Panel       │◄──►│    AI Assistant Panel     │  │
│  │  InteractionDetails   │    │  ChatHistory              │  │
│  │  TopicsSection        │    │  SuggestionChips          │  │
│  │  MaterialsSection     │    │  ChatInput (+ mic)        │  │
│  │  SentimentSelector    │    │                           │  │
│  │  OutcomesSection      │    │  useChatStream hook       │  │
│  │  FollowUpSection      │    │  (SSE reader)             │  │
│  │  FormActions          │    └───────────────────────────┘  │
│  └───────────────────────┘                                   │
│           Redux Store: formSlice + chatSlice                 │
└───────────────────────────┬──────────────────────────────────┘
                            │ HTTP + SSE
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                         │
│                                                              │
│  POST /api/chat ──► chat.py                                  │
│    ├─ confirmation?  ──► log_interaction tool                │
│    ├─ list query?    ──► list_interactions tool              │
│    ├─ edit query?    ──► find_interaction + edit_interaction  │
│    └─ default        ──► LLM extraction → confirmation prompt│
│                                                              │
│  POST /api/transcribe ──► Groq Whisper                       │
│  /api/hcps, /api/interactions ──► CRUD routers               │
└───────────────────────────┬──────────────────────────────────┘
                            │ SQLAlchemy ORM
              ┌─────────────┴───────────────┐
              │                             │
              ▼                             ▼
   ┌──────────────────┐          ┌──────────────────┐
   │   PostgreSQL DB  │          │    Groq API       │
   │  hcps            │          │  llama-3.3-70b    │
   │  interactions    │          │  whisper-large-v3 │
   └──────────────────┘          └──────────────────┘
```

### Streaming Chat Flow

```
User message
    │
    ▼
POST /api/chat  (SSE response)
    │
    ├── _is_confirmation()? ──► log_interaction ──► DB write
    │                            suggest_followup
    │                               │
    ├── _is_list_query()? ──► list_interactions tool
    │                               │
    ├── _is_edit_previous_query()? ─► find_interaction
    │                                 edit_interaction
    │                               │
    └── default ──► LLM extract + show summary (no DB write)
                              │
              SSE chunks: { type: "text" | "form_update" | "suggestions" | "done" }
```

---

## Features

| Feature | Description |
|---------|-------------|
| **Natural language logging** | Free-text interaction description → structured DB record |
| **Real-time form population** | Form fields animate and fill as the AI streams |
| **Two-phase save** | AI shows summary first; saves to DB only after "yes" |
| **Voice input** | Mic button records audio; Groq Whisper transcribes it |
| **Interaction retrieval** | "Show my interactions this week" → formatted list |
| **Inline editing** | "Change sentiment of today's Dr. Kim visit to positive" |
| **Follow-up suggestions** | 3 AI-generated follow-up chips after every save |
| **HCP autocomplete** | Debounced typeahead search against the HCP database |
| **AI highlight animation** | Gold flash on form fields when AI populates them |
| **Panel toggle** | Hide/show the form panel to maximize chat space |

---

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend framework | React | 19 |
| State management | Redux Toolkit + React-Redux | 2.x |
| Styling | Tailwind CSS | 3.4 |
| Build tool | Vite | 8 |
| HTTP client | Axios | 1.x |
| Backend framework | FastAPI | 0.115 |
| ORM | SQLAlchemy | 2.0 |
| Migrations | Alembic | 1.13 |
| Data validation | Pydantic v2 | 2.9 |
| ASGI server | Uvicorn | 0.30 |
| LLM | Groq — `llama-3.3-70b-versatile` | — |
| Suggestions LLM | Groq — `llama-3.1-8b-instant` | — |
| Speech-to-text | Groq Whisper — `whisper-large-v3-turbo` | — |
| Agent framework | LangChain / LangGraph | 0.3.x / 0.2.x |
| Database | PostgreSQL 16 | — |
| Streaming protocol | Server-Sent Events (SSE) | — |

---

## Project Structure

```
ai-crm-hcp/
│
├── backend/                         # FastAPI application
│   ├── app/
│   │   ├── main.py                  # App entry, CORS, lifespan, router registration
│   │   ├── config.py                # Pydantic settings (env vars)
│   │   ├── database.py              # SQLAlchemy engine, session factory, get_db
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── hcp.py               # HCP ORM model
│   │   │   └── interaction.py       # Interaction ORM model
│   │   ├── schemas/
│   │   │   ├── hcp.py               # HCPCreate, HCPRead
│   │   │   ├── interaction.py       # InteractionCreate, InteractionUpdate, InteractionRead
│   │   │   └── chat.py              # ChatMessage, ChatRequest
│   │   ├── routers/
│   │   │   ├── hcps.py              # GET/POST /api/hcps
│   │   │   ├── interactions.py      # CRUD /api/interactions
│   │   │   ├── chat.py              # POST /api/chat (SSE streaming)
│   │   │   └── transcribe.py        # POST /api/transcribe (Whisper)
│   │   └── agent/
│   │       └── tools/
│   │           ├── log_interaction.py    # Extract fields + save to DB
│   │           ├── edit_interaction.py   # Edit a field via natural language
│   │           ├── list_interactions.py  # List by period (today/week/month/all)
│   │           ├── find_interaction.py   # Find interaction for editing
│   │           ├── suggest_followup.py   # Generate follow-up suggestions
│   │           └── search_hcp.py         # HCP name lookup
│   ├── alembic/
│   │   └── versions/                # Migration scripts
│   ├── tests/
│   │   ├── conftest.py              # SQLite test DB fixture
│   │   ├── test_hcps.py
│   │   ├── test_interactions.py
│   │   └── agent/
│   │       ├── test_log_interaction.py
│   │       └── test_search_hcp.py
│   ├── seed.py                      # Seed test HCP data
│   ├── requirements.txt
│   ├── Procfile                     # Heroku: uvicorn start command
│   ├── railway.json                 # Railway.app deployment config
│   ├── alembic.ini
│   ├── .env                         # Local env vars (gitignored)
│   └── .env.example                 # Env var template
│
├── frontend/                        # React application
│   ├── src/
│   │   ├── main.jsx                 # React DOM entry point
│   │   ├── App.jsx                  # Root component
│   │   ├── index.css                # Global styles + Tailwind directives
│   │   ├── api/
│   │   │   └── client.js            # Axios instance (baseURL from VITE_API_URL)
│   │   ├── store/
│   │   │   ├── index.js             # Redux store setup
│   │   │   ├── chatSlice.js         # Chat state (messages, streaming, suggestions)
│   │   │   └── formSlice.js         # Form state (all interaction fields, AI highlights)
│   │   ├── hooks/
│   │   │   └── useChatStream.js     # SSE streaming hook — reads chat SSE, dispatches actions
│   │   └── components/
│   │       ├── LogInteractionPage.jsx   # Top-level page layout
│   │       ├── AIAssistantPanel/
│   │       │   ├── index.jsx            # Panel container
│   │       │   ├── ChatHistory.jsx      # Message list (user + assistant)
│   │       │   ├── ChatInput.jsx        # Textarea + mic + send
│   │       │   └── SuggestionChips.jsx  # Clickable follow-up chips
│   │       └── FormPanel/
│   │           ├── index.jsx            # Panel container + scroll
│   │           ├── InteractionDetails.jsx  # HCP search, type, date, time, attendees
│   │           ├── TopicsSection.jsx       # Topics discussed textarea
│   │           ├── MaterialsSection.jsx    # Materials shared + samples distributed
│   │           ├── SentimentSelector.jsx   # Positive / Neutral / Negative radio
│   │           ├── OutcomesSection.jsx     # Outcomes textarea
│   │           ├── FollowUpSection.jsx     # Follow-up actions + date
│   │           └── FormActions.jsx         # Save Log + Cancel buttons + Toast
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── .env                         # VITE_API_URL (gitignored)
│
├── docker-compose.yml               # Local PostgreSQL via Docker
└── README.md                        # This file
```

---

## Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **PostgreSQL** — local via Docker (below) or a cloud provider like [Neon](https://neon.tech)
- **Groq API key** — free at [console.groq.com](https://console.groq.com)

---

## Quick Start

### 1. Clone

```bash
git clone <repo-url>
cd ai-crm-hcp
```

### 2. Start PostgreSQL (Docker)

```bash
docker-compose up -d
# Starts PostgreSQL at localhost:5433
# DB: ai_crm  |  User: crm  |  Password: crm_secret
```

### 3. Backend

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Open .env and fill in DATABASE_URL and GROQ_API_KEY

# Apply database migrations
alembic upgrade head

# (Optional) Seed test HCP data
python seed.py

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# API available at http://localhost:8000
# Swagger UI at  http://localhost:8000/docs
```

### 4. Frontend

```bash
cd frontend

npm install

# Create .env
echo "VITE_API_URL=http://localhost:8000" > .env

npm run dev
# App available at http://localhost:5173
```

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | — | PostgreSQL connection string |
| `GROQ_API_KEY` | Yes | — | Groq API authentication key |
| `ALLOWED_ORIGINS` | No | `http://localhost:5173` | Comma-separated CORS allowed origins |

```env
DATABASE_URL=postgresql://crm:crm_secret@localhost:5433/ai_crm
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ALLOWED_ORIGINS=http://localhost:5173
```

### Frontend (`frontend/.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `VITE_API_URL` | No | `http://localhost:8000` | Backend API base URL |

```env
VITE_API_URL=http://localhost:8000
```

---

## API Overview

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check — returns `{"status":"ok"}` |
| `POST` | `/api/chat` | Streaming AI chat (SSE) |
| `POST` | `/api/transcribe` | Audio file → transcribed text (Whisper) |
| `GET` | `/api/hcps` | List HCPs, optional `?q=` search |
| `POST` | `/api/hcps` | Create HCP |
| `GET` | `/api/hcps/{id}` | Get HCP by ID |
| `GET` | `/api/interactions` | List interactions, optional `?hcp_id=` filter |
| `POST` | `/api/interactions` | Create interaction |
| `GET` | `/api/interactions/{id}` | Get interaction by ID |
| `PATCH` | `/api/interactions/{id}` | Partial update interaction |
| `DELETE` | `/api/interactions/{id}` | Delete interaction |

Interactive API docs: `http://localhost:8000/docs`

---

## Database Schema

### `hcps`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | `VARCHAR(36)` | Primary key (UUID) |
| `name` | `VARCHAR(255)` | NOT NULL |
| `specialty` | `VARCHAR(100)` | Nullable |
| `territory` | `VARCHAR(100)` | Nullable |
| `email` | `VARCHAR(255)` | Nullable |
| `phone` | `VARCHAR(50)` | Nullable |
| `created_at` | `TIMESTAMP` | Default UTC now |

### `interactions`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | `VARCHAR(36)` | Primary key (UUID) |
| `hcp_id` | `VARCHAR` | FK → `hcps.id` (SET NULL on delete) |
| `interaction_type` | `VARCHAR(50)` | Default "Meeting" |
| `date` | `DATE` | NOT NULL |
| `time` | `TIME` | Nullable |
| `attendees` | `JSON` | Array of strings |
| `topics_discussed` | `TEXT` | Nullable |
| `materials_shared` | `JSON` | Array of strings |
| `samples_distributed` | `JSON` | Array of strings |
| `sentiment` | `VARCHAR(20)` | `positive` / `neutral` / `negative` |
| `outcomes` | `TEXT` | Nullable |
| `follow_up_actions` | `TEXT` | Nullable |
| `follow_up_date` | `DATE` | Nullable |
| `raw_chat_summary` | `TEXT` | Original conversation text |
| `created_at` | `TIMESTAMP` | Default UTC now |
| `updated_at` | `TIMESTAMP` | Auto-updated UTC now |

---

## Deployment

### Backend — Railway

```bash
# railway.json is pre-configured for Nixpacks build
# Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
# Health check: GET /health

# Set these environment variables in Railway dashboard:
DATABASE_URL=postgresql://...?sslmode=require
GROQ_API_KEY=gsk_...
ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

### Backend — Heroku

```bash
# Procfile is pre-configured:
# web: uvicorn app.main:app --host 0.0.0.0 --port $PORT

heroku config:set DATABASE_URL=... GROQ_API_KEY=... ALLOWED_ORIGINS=...
git push heroku main
```

### Frontend — Vercel / Netlify

```
Build command:    npm run build
Output directory: dist
Environment:      VITE_API_URL=https://your-backend-url
```

### Run migrations in production

```bash
alembic upgrade head
```
#   A I - C R M  
 