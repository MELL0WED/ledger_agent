import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.embeddings.embedder import generate_text_embedding
from dotenv import load_dotenv

load_dotenv()

# Connect to the live distributed Qdrant engine running inside Docker
qdrant_db = QdrantClient(
    host=os.getenv("QDRANT_HOST", "127.0.0.1"),
    port=int(os.getenv("QDRANT_PORT", 6333))
)
COLLECTION_NAME = "compliance_policies"

def init_qdrant_vector_store():
    """Forces creation and seeding of our live containerized collection index."""
    try:
        # Atomic recreation pattern: drop if collection exists to clear invalid schema footprints
        try:
            qdrant_db.delete_collection(collection_name=COLLECTION_NAME)
        except Exception:
            pass # Collection did not exist previously
            
        # Recreate clean collection index mapping parameters
        qdrant_db.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        
        # Seed unstructured enterprise compliance directives
        policies = [
            "Policy Notice: Acme Corp pricing profiles allow a maximum 5% processing fee variance.",
            "System Log: Purchase order reference PO-9902 requires strict routing to Delta Labs auditing division."
        ]
        
        points = []
        for idx, text in enumerate(policies):
            vector = generate_text_embedding(text)
            points.append(PointStruct(
                id=idx,
                vector=vector,
                payload={"policy_text": text}
            ))
            
        qdrant_db.upsert(collection_name=COLLECTION_NAME, points=points)
        print(" -> [QDRANT INDEX SETUP] Collection recreated and populated successfully.")
    except Exception as e:
        print(f" -> [QDRANT ERROR] Failure generating collection index: {str(e)}")
        raise e

def search_compliance_vectors(query_text: str, limit: int = 1) -> list:
    """Performs a semantic similarity search across our live compliance index using modern query parameters."""
    query_vector = generate_text_embedding(query_text)
    
    search_result = qdrant_db.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit
    )
    
    return [hit.payload["policy_text"] for hit in search_result.points]
