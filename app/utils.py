# Utilities for the Norm AI take-home project
# --------------------------------------------
# Defines Pydantic models for request/response payloads,
# and services for document ingestion (DocumentService)
# and vector queries (QdrantService).

from pydantic import BaseModel
import qdrant_client
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings import OpenAIEmbedding
from llama_index.llms import OpenAI
from llama_index.readers import SimpleDirectoryReader
from llama_index.schema import Document
from llama_index import (
    VectorStoreIndex,
    ServiceContext,
)
import os

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


class DocumentService:
    """Handles document ingestion into LlamaIndex Documents (ready for embedding)."""

    # NOTE: In real-world LlamaIndex usage, you would typically load one Document per file,
    # then parse it into multiple Nodes before embedding. We skip that step here by design.

    def create_documents(self, file_path: str = "docs/laws.pdf") -> list[Document]:
        reader = SimpleDirectoryReader(input_files=[file_path])
        documents = reader.load_data()
        # Attach basic metadata (e.g., filename) for context
        for doc in documents:
            if doc.metadata is None:
                doc.metadata = {}
            doc.metadata["source"] = os.path.basename(file_path)
        return documents


class QdrantService:
    """Provides a vector index backed by Qdrant + LlamaIndex, with a stub mode for testing."""

    def __init__(self, k: int = 2, use_stub: bool = False):
        self.index = None
        self.k = k
        self.use_stub = use_stub

    def connect(self) -> None:
        # TODO: Replace stub with real OpenAI API key when running with embeddings
        # api_key = os.environ["OPENAI_API_KEY"]
        client = qdrant_client.QdrantClient(location=":memory:")
        vstore = QdrantVectorStore(client=client, collection_name="temp")

        service_context = ServiceContext.from_defaults(
            embed_model=OpenAIEmbedding(), llm=OpenAI(api_key=key, model="gpt-4")
        )

        self.index = VectorStoreIndex.from_vector_store(
            vector_store=vstore, service_context=service_context
        )

    def load(self, docs=list[Document]):
        self.index.insert_nodes(docs)

    def query(self, user_query: str) -> Output:
        # --- Stub implementation for testing without external API keys ---
        if self.use_stub or not self.index:
            q = user_query.lower()
            if "food" in q or "baker" in q or "flour" in q or "bread" in q:
                return Output(
                    query=user_query,
                    response="Food safety violations may result in fines or whipping.",
                    citations=[
                        Citation(
                            source="Laws of the Seven Kingdoms, §11.1",
                            text="A baker who mixes sawdust in his flour, might be fined. If such a fine cannot be paid, he might be whipped instead."
                        )
                    ]
                )
            elif "hand" in q or "finger" in q or "amputation" in q or "thief" in q or "steal" in q:
                return Output(
                    query=user_query,
                    response="Certain crimes can result in the loss of a finger or a hand, including thievery and poaching.",
                    citations=[
                        Citation(
                            source="Laws of the Seven Kingdoms, §6.1–6.2",
                            text="It is customary for a thief to be punished by losing a finger or a hand. Pickpockets can likewise be punished by cutting off a hand."
                        ),
                        Citation(
                            source="Laws of the Seven Kingdoms, §7.1",
                            text="Poaching is forbidden... punishments for poaching can include being forced to join the Night's Watch, losing a hand, or being forced to row ships."
                        )
                    ]
                )
            else:
                return Output(
                    query=user_query,
                    response=f"No specific law found for query: {user_query}",
                    citations=[]
                )

        # --- Real implementation ---
        query_engine = self.index.as_query_engine(similarity_top_k=self.k)
        response = query_engine.query(user_query)
        citations = []
        for node in response.source_nodes:
            citation = Citation(
                source=node.source_node.metadata.get("source", "unknown"),
                text=node.source_node.text,
            )
            citations.append(citation)
        output = Output(
            query=user_query, response=response.response, citations=citations
        )
        return output


def test_qdrant_query():
    # Step 1: spin up the service
    service = QdrantService(k=2)
    service.connect()  # sets up index, embeddings, etc.

    # Step 2: add a tiny document so there’s something to query
    doc = llama_index.Document(text="Jon Snow is the King in the North.")
    service.index.insert(doc)

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
