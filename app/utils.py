# Utilities for the Norm AI take-home project
# --------------------------------------------
# Defines Pydantic models for request/response payloads,
# and services for document ingestion (DocumentService)
# and vector queries (QdrantService).

from pydantic import BaseModel
import qdrant_client
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    ServiceContext,
)
from llama_index.core.schema import Document
from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
import os
import re

# TODO: Use OpenAI API key from environment when running real embeddings
# Example: os.environ["OPENAI_API_KEY"]

# -----------------
# Pydantic models
# -----------------


class Input(BaseModel):
    query: str
    file_path: str


class Citation(BaseModel):
    source: str
    text: str


class Output(BaseModel):
    query: str
    response: str
    citations: list[Citation]


# -----------------
# Services
# -----------------



class LoggingEmbedding(OpenAIEmbedding):
    def _get_embeddings(self, texts):
        print(f"[LOG] Sending embedding request with {len(texts)} chunks")
        for t in texts[:3]:  # show first 3 for sanity
            print(f"    chunk preview: {t[:60]!r}...")
        return super()._get_embeddings(texts)
    


class DocumentService:
    def create_documents(self, file_path: str = "docs/laws.pdf") -> list[Document]:
        reader = SimpleDirectoryReader(input_files=[file_path])
        documents = reader.load_data()
        full_text = "\n".join([doc.text for doc in documents])

        # Cut off citations section
        full_text = re.split(r"\nCitations:", full_text)[0]

        # Split into top-level law sections (like 1. Peace, 2. Religion...)
        top_sections = re.split(r"\n(?=\d+\.\s)", full_text)

        docs = []
        for section in top_sections:
            section = section.strip()
            if not section:
                continue

            lines = section.splitlines()
            title = lines[0]

            # Split into first-level subclauses (like 6.1, 6.2, but keep deeper nesting with them)
            subclauses = re.split(r"\n(?=\d+\.\d+\s)", section)
            for clause in subclauses:
                clause = clause.strip()
                if not clause or clause == title:
                    continue

                first_line = clause.splitlines()[0]
                metadata = {
                    "source": os.path.basename(file_path),
                    "section": title,
                    "clause": first_line,
                }
                docs.append(Document(text=clause, metadata=metadata))

        return docs


class QdrantService:
    """Provides a vector index backed by Qdrant + LlamaIndex, with a stub mode for testing."""

    def __init__(self, k: int = 2, use_stub: bool = False):
        self.index = None
        self.client = None
        self.k = k
        self.use_stub = use_stub

    def connect(self) -> None:
        """Initialize Qdrant client + service context. Index starts empty until load() is called."""
        api_key = os.environ["OPENAI_API_KEY"]

        # Direct connection to Qdrant (not through QdrantVectorStore wrapper)
        self.client = qdrant_client.QdrantClient(
            url=os.environ.get("QDRANT_URL", "http://localhost:6333"),
            api_key=os.environ.get("QDRANT_API_KEY"),
        )

        service_context = ServiceContext.from_defaults(
            embed_model = OpenAIEmbedding(
                model_name="text-embedding-3-small",
                batch_size=32,          # efficient batching
                max_retries=5           # exponential backoff on 429s
            ),
        )
        # Build an *empty* index to start with — documents will be added via load()
        self.index = VectorStoreIndex.from_documents(
            [],  # empty list initially
            service_context=service_context,
        )

    def load(self, docs: list[Document]):
        """Insert new documents into the index."""
        if not self.index:
            raise RuntimeError("Index not initialized. Did you run connect()?")

        self.index.insert_nodes(docs)

    def query(self, user_query: str) -> Output:
        """Query the index or fall back to stubbed response."""
        if self.use_stub:
            return Output(
                query=user_query,
                response=f"[Stubbed answer for '{user_query}']",
                citations=[],
            )

        if not self.index:
            raise RuntimeError("Index not initialized. Did you run connect()?")

        query_engine = self.index.as_query_engine(similarity_top_k=self.k)
        response = query_engine.query(user_query)

        citations = [
            Citation(
                source=node.node.metadata.get("source", "unknown"),
                text=node.node.text,
            )
            for node in response.source_nodes
        ]

        return Output(
            query=user_query,
            response=response.response,
            citations=citations,
        )




def test_qdrant_query():
    # Step 1: spin up the service
    service = QdrantService(k=2)
    service.connect()  # sets up index, embeddings, etc.

    # Step 2: add a tiny document using .load() so embeddings run
    doc = Document(text="Jon Snow is the King in the North.", metadata={"source": "test"})
    service.load([doc])   # <-- use load(), not insert()

    # Step 3: run a query
    output = service.query("Who is Jon Snow?")

    # Step 4: print results to check shape
    print("QUERY:", output.query)
    print("RESPONSE:", output.response)
    print("CITATIONS:")
    for c in output.citations:
        print("  -", c)


if __name__ == "__main__":
    # Smoke test: load a document and print preview
    service = DocumentService()
    docs = service.create_documents("docs/laws.pdf")
    print(f"Loaded {len(docs)} docs. First 300 chars:\n{docs[0].text[:300]}")
    print("Metadata:", docs[0].metadata)

    # Optional manual workflow test (requires real keys + Qdrant)
    # index = QdrantService()
    # index.connect()
    # index.load(docs)
    # print(index.query("what happens if I steal?"))
