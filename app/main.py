# app/main.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from app.utils import Output, QdrantService, DocumentService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the service once
service = QdrantService(k=2)

@app.on_event("startup")
async def startup_event():
    """Initialize vector service on app startup (safe mode)."""
    try:
        service.connect()
        # Load documents so embeddings actually run
        docs = DocumentService().create_documents("docs/laws.pdf")
        service.load(docs)
        print(f"✅ QdrantService initialized with {len(docs)} docs")
    except Exception as e:
        # Fail gracefully into stub mode
        service.use_stub = True
        print(f"⚠️ Falling back to stub mode: {e}")

@app.get("/search", response_model=Output)
async def search(query: str = Query(..., description="Search query string")):
    """Accepts a query string and returns a structured Output response."""
    try:
        return service.query(query)
    except Exception as e:
        # Always return *something* instead of crashing
        return Output(
            query=query,
            response=f"[Stub response due to error: {e}]",
            citations=[],
        )
