from app.database.qdrant_client import init_qdrant_vector_store
print("Initializing Qdrant Vector Collection Index inside Docker container...")
init_qdrant_vector_store()
print("Databases synced successfully.")