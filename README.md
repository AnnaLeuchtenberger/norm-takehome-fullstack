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
GET http://127.0.0.1:8000/search?query=bread
```

```json
{
  "query": "bread",
  "response": "Food safety violations may result in fines or whipping.",
  "citations": [
    {
      "source": "Laws of the Seven Kingdoms, §11.1",
      "text": "A baker who mixes sawdust in his flour, might be fined. If such a fine cannot be paid, he might be whipped instead."
    }
  ]
}
```


---

## Design Choices & Assumptions
- **Proof of Concept** This project assumes it is a proof of concept for the client, and that the functionality expectations will stay within clearly delimited guardrails during the demo.- **Stubbed Qdrant:** As such, the service runs in stub mode by default. *No OpenAI or Qdrant API keys are required* for this exercise.  
- **Stubbed Responses:**  
  - The backend currently supports two canned answers:  
    - **Baker response:** triggered by the keywords `"food"`, `"baker"`, `"flour"`, or `"bread"`.  
    - **Thief response:** triggered by the keywords `"hand"`, `"finger"`, `"amputation"`, `"thief"`, or `"steal"`.  
  - If a query matches one of these keyword sets, the service returns the corresponding canned JSON response (see above).  
  - Any other query will return an empty `results` array.  
  - Combining these two queries is currently not supported.
- **Lightweight:** The API is designed to be as lightweight as possible — a single `/search` endpoint returning a typed `Output` model. 
- **Swagger Testing:** Reviewers are expected to test via the built-in Swagger docs rather than curl/Postman.  
- **Containerization:** Docker support is included for a consistent runtime environment. 
---

## Client
See the `frontend` folder for the Next.js client, which demonstrates calling this service. It has its own README with setup instructions.