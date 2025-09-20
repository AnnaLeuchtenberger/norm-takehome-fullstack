# FastAPI entrypoint: exposes a /search endpoint that wraps QdrantService
# Returns results serialized into the Output Pydantic model

from fastapi import FastAPI, Query
from app.utils import Output, QdrantService

app = FastAPI()
service = QdrantService()  # stub mode: works without external API keys


@app.get("/search", response_model=Output)
async def search(query: str = Query(..., description="Search query string")):
    """Accepts a query string and returns a structured Output response."""
    return service.query(query)
