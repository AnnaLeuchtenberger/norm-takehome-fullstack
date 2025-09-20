# Norm AI Take-Home — Server

This repository implements a FastAPI service that ingests a PDF of laws (`docs/laws.pdf`), indexes them into Qdrant, and exposes a simple search endpoint.

## Running the Application

### Prerequisites
- Python 3.11+
- [Poetry](https://python-poetry.org/) or `pip` / `venv`
- Docker (optional, if you want to run inside a container)

### Local Development

1. **Clone the repo and install dependencies**
   ```bash
   git clone https://github.com/AnnaLeuchtenberger/norm-takehome-fullstack.git
   cd norm-takehome-fullstack
   poetry install   # or: pip install -r requirements.txt
   ```

2. **Start the FastAPI server**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Open the Swagger docs**
   Once running, navigate to:
   ```
   http://127.0.0.1:8000/docs
   ```
   You can use this interactive UI to issue queries against the `/search` endpoint.

### Using Docker
1. **Build the image:**
   ```bash
   docker build -t norm-server .
   ```
2. **Run the container:**
   ```bash
   docker run -p 8000:8000 norm-server
   ```
3. Visit Swagger at [http://localhost:8000/docs](http://localhost:8000/docs).

## Querying the Service
- **Endpoint:** `GET /search`  
- **Parameter:** `query` (string) — the search query  
- **Response:** JSON containing matching results from Qdrant (*stubbed unless a real API key is configured*)  

Example request:
```
GET http://127.0.0.1:8000/search?query=peace
```

```json
{
  "results": [
    {
      "text": "The law requires petty lords and landed knights to take their disputes to court.",
      "score": 0.87
    }
  ]
}
```
<!-- TODO: Replace this example output with the actual stubbed response from your QdrantService if it looks different -->

---

## Design Choices & Assumptions
- **Stubbed Qdrant:** By default, the service runs in stub mode. *No OpenAI or Qdrant API keys are required* for this exercise.  
- **Simple contract:** The API is intentionally minimal — a single `/search` endpoint returning a typed `Output` model.  
- **Swagger as client:** Reviewers are expected to test via the built-in Swagger docs rather than curl/Postman.  
- **Containerization:** Docker support is included for a consistent runtime environment.  

---

## Client
See the `frontend` folder for the Next.js client, which demonstrates calling this service. It has its own README with setup instructions.