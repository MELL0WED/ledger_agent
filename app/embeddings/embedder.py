from sentence_transformers import SentenceTransformer

# Initialize model locally on CPU execution thread
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_text_embedding(text: str) -> list:
    """Transforms raw document payloads into a 384-dimensional floating point vector."""
    embedding = embedding_model.encode(text, convert_to_numpy=True)
    return embedding.tolist()
