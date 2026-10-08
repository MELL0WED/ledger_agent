import asyncio
from evaluation.evaluator_async import run_scale_stress_test
from app.database.qdrant_client import init_qdrant_vector_store

if __name__ == "__main__":
    print("====================================================")
    print("BOOSTRAPPING CONTAINERIZED SYSTEM STATE WORKSPACE")
    print("====================================================")
    
    try:
        init_qdrant_vector_store()
        print(" -> Qdrant cluster baseline handshake: SUCCESS\n")
    except Exception as e:
        print(f" -> CRITICAL: Qdrant setup failed: {e}\n")
        
    # Launch high-capacity async scale metric processing harness
    asyncio.run(run_scale_stress_test("evaluation/test_bench_large.json", concurrency_limit=3))
