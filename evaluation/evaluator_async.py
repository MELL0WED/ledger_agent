import json
import time
import asyncio
from app.main import execute_ledger_agent

async def worker_node(case: dict, semaphore: asyncio.Semaphore):
    """Executes a single workflow loop within a globally isolated rate-limiting frame."""
    async with semaphore:
        # Run blocking agent architecture execution loops smoothly inside an async wrapper thread
        loop = asyncio.get_running_loop()
        start = time.perf_counter()
        
        try:
            agent_output = await loop.run_in_executor(None, execute_ledger_agent, case['text'])
            latency = time.perf_counter() - start
            
            is_correct_route = agent_output.get("routing_path") == case["expected_routing"]
            is_schema_valid = agent_output.get("extraction_error") is None and agent_output.get("extracted_data") is not None
            
            return {
                "success": True,
                "latency": latency,
                "correct_route": is_correct_route,
                "schema_valid": is_schema_valid,
                "cache_hit": "CACHE HIT" in str(agent_output.get("resolution_log", ""))
            }
        except Exception as e:
            return {"success": False, "error": str(e), "latency": time.perf_counter() - start}

async def run_scale_stress_test(test_bench_path: str, concurrency_limit: int = 20):
    print("====================================================")
    print(f"STARTING MASSIVE ASYNC AGENT SYSTEM PROFILING LEDGER")
    print("====================================================\n")
    
    with open(test_bench_path, 'r') as f:
        test_cases = json.load(f)
        
    semaphore = asyncio.Semaphore(concurrency_limit)
    tasks = [worker_node(case, semaphore) for case in test_cases]
    
    global_start = time.perf_counter()
    results = await asyncio.gather(*tasks)
    global_duration = time.perf_counter() - global_start
    
    # Process Metrics Analytics
    valid_results = [r for r in results if r.get("success")]
    total_processed = len(valid_results)
    
    if total_processed == 0:
        print("CRITICAL ERROR: All async execution routines aborted/failed.")
        return
        
    schema_adherences = sum(1 for r in valid_results if r["schema_valid"])
    correct_routes = sum(1 for r in valid_results if r["correct_route"])
    latencies = [r["latency"] for r in valid_results]
    
    throughput_rps = total_processed / global_duration
    
    print("====================================================")
    print("         LARGE-SCALE SYSTEM METRICS AT SCALE        ")
    print("====================================================")
    print(f"Total Scaled Load Volume  : {total_processed} items")
    print(f"Global Stress Test Time   : {global_duration:.2f} seconds")
    print(f"System Throughput Capacity: {throughput_rps:.2f} Requests/Sec (RPS)")
    print(f"Schema Adherence Rate     : {(schema_adherences / total_processed)*100:.1f}%")
    print(f"State Routing Accuracy    : {(correct_routes / total_processed)*100:.1f}%")
    print(f"Average Pipeline Latency  : {sum(latencies)/total_processed:.3f} seconds")
    print("====================================================\n")

if __name__ == "__main__":
    asyncio.run(run_scale_stress_test("evaluation/test_bench_large.json", concurrency_limit=20))
