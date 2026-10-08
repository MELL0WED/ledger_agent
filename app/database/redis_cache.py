import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize connection pool to local Windows Redis Server instance
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=True
)

def get_semantic_cache(cache_key: str) -> dict:
    """Retrieves cached transaction payloads using structural hash values."""
    cached_data = redis_client.get(f"cache:ledger:{cache_key}")
    if cached_data:
        return json.loads(cached_data)
    return None

def set_semantic_cache(cache_key: str, data: dict, ttl: int = 3600):
    """Caches validated structures with an explicit time-to-live expiration flag."""
    redis_client.setex(
        f"cache:ledger:{cache_key}",
        ttl,
        json.dumps(data)
    )
