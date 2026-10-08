# Save as D:\ledger_agent\flush_cache.py
import redis

try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.flushall()
    print(" -> SUCCESS: Local Redis cluster context flushed completely.")
except Exception as e:
    print(f" -> Error flushing cache: {e}")
