# FastAPI entrypoint: exposes a /search endpoint that wraps QdrantService
# Returns results serialized into the Output Pydantic model

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from app.utils import Output, QdrantService

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
service = QdrantService()  # stub mode: works without external API keys


@app.get("/search", response_model=Output)
async def search(query: str = Query(..., description="Search query string")):
    """Accepts a query string and returns a structured Output response."""
    return service.query(query)
