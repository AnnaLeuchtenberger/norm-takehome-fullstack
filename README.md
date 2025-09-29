# Norm AI Take-Home — Fullstack Demo

This project implements a FastAPI service that ingests a PDF of laws (`docs/laws.pdf`), indexes them into Qdrant using OpenAI embeddings, and exposes a `/search` endpoint.  
A lightweight Next.js frontend is included to demonstrate querying the service and displaying results with citations.

---

## Running the Backend

### Option 1: Local (Python)

**Prerequisites**  
- Python 3.11  
- `pip` (or Poetry/venv if you prefer)

```bash
git clone https://github.com/AnnaLeuchtenberger/norm-takehome-fullstack.git
cd norm-takehome-fullstack
pip install -r requirements.txt
export OPENAI_API_KEY=sk-proj...   # your API key
uvicorn app.main:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).  
Swagger docs are at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

### Option 2: Docker

**Prerequisites**  
- Docker

```bash
docker build -t norm-fullstack .
docker run -e OPENAI_API_KEY=sk-proj... -p 8000:8000 norm-fullstack
```

Then visit [http://localhost:8000/docs](http://localhost:8000/docs) to interact with the API.

---

## Querying the Backend

**Endpoint:**  
```
GET /search?query=your+question
```

**Example:**  
```bash
curl "http://127.0.0.1:8000/search?query=steal"
```

**Example Response:**  
```json
{
  "query": "steal",
  "response": "Those who engage in stealing may face punishments such as losing a finger or a hand...",
  "citations": [
    {
      "source": "laws.pdf",
      "text": "6. Thievery\n6.1. It is customary for a thief..."
    }
  ]
}
```

---

## Running the Frontend

The `frontend` folder contains a Next.js app that calls the backend and displays results.

**Local development:**

```bash
cd frontend
npm install --legacy-peer-deps   # resolves peer dependency conflicts
npm run dev
```

The app will be live at [http://localhost:3000](http://localhost:3000).  
It will send queries to the backend running at [http://127.0.0.1:8000/search].

---

## Reviewer Quick Start

If you just want to see it running end-to-end:

1. **Start backend in Docker:**
   ```bash
   docker build -t norm-fullstack .
   docker run -e OPENAI_API_KEY=sk-... -p 8000:8000 norm-fullstack
   ```
2. **Start frontend in dev mode:**
   ```bash
   cd frontend
   npm install --legacy-peer-deps
   npm run dev
   ```
3. Open:
   - [http://localhost:3000](http://localhost:3000) → frontend demo UI  
   - [http://localhost:8000/docs](http://localhost:8000/docs) → backend Swagger UI  

---

## Design Choices

- **Document parsing:** `laws.pdf` is split into top-level sections (e.g., “6. Thievery”) and first-level clauses (e.g., “6.1”, “6.2”), while deeper subclauses remain grouped together for context.  
- **Backend:** FastAPI service with a single `/search` endpoint, returning structured `Output` objects with response + citations.  
- **Vector storage:** Qdrant is used as the vector index; embeddings are generated with OpenAI’s `text-embedding-3-small`.  
- **LLM synthesis:** Responses are generated with `gpt-3.5-turbo`, combining retrieved clauses into a natural-language answer.  
- **Frontend:** Simple Next.js UI with prefilled example queries and a display of citations for transparency.  
- **Containerization:** Docker image provided for consistent backend setup.

---
