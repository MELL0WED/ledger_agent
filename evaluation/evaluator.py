import json
import time
from app.main import execute_ledger_agent

def run_system_evaluation(test_bench_path: str):
    print("====================================================")
    print("STARTING MULTI-AGENT STATE MACHINE SYSTEM PROFILING")
    print("====================================================\n")
    
    with open(test_bench_path, 'r') as f:
        test_cases = json.load(f)
        
    total_cases = len(test_cases)
    successful_schema_adherences = 0
    correct_routing_decisions = 0
    execution_latencies = []
    
    for case in test_cases:
        print(f"Processing Test Case #{case['id']}...")
        
        start_time = time.perf_counter()
        agent_output = execute_ledger_agent(case['text'])
        end_time = time.perf_counter()
        
        latency = end_time - start_time
        execution_latencies.append(latency)
        
        # 1. Measure Schema Adherence (Did it crash or fail Pydantic validation?)
        if agent_output.get("extraction_error") is None and agent_output.get("extracted_data") is not None:
            successful_schema_adherences += 1
            
        # 2. Measure Routing Precision (Did it route to the correct termination node?)
        actual_routing = agent_output.get("routing_path")
        if actual_routing == case["expected_routing"]:
            correct_routing_decisions += 1
            print(f" -> Success: Routed to '{actual_routing}' in {latency:.3f}s")
        else:
            print(f" -> MISMATCH: Expected '{case['expected_routing']}', got '{actual_routing}'")
            
        print("-" * 50)
        
    # Calculate System Performance Indicators
    schema_adherence_rate = (successful_schema_adherences / total_cases) * 100
    routing_accuracy = (correct_routing_decisions / total_cases) * 100
    avg_latency = sum(execution_latencies) / total_cases
    min_latency = min(execution_latencies)
    
    print("\n====================================================")
    print("             SYSTEM EVALUATION METRICS              ")
    print("====================================================")
    print(f"Total Evaluated Scenarios : {total_cases}")
    print(f"Schema Adherence Rate     : {schema_adherence_rate:.1f}%")
    print(f"State Routing Accuracy   : {routing_accuracy:.1f}%")
    print(f"Average Pipeline Latency  : {avg_latency:.3f} seconds")
    print(f"Peak Execution Latency    : {min_latency:.3f} seconds")
    print("====================================================\n")
    
    return {
        "schema_adherence": schema_adherence_rate,
        "routing_accuracy": routing_accuracy,
        "avg_latency": avg_latency
    }
