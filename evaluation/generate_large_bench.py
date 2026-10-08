import json
import random

def generate_enterprise_test_suite(output_path: str, count: int = 1000):
    print(f"Generating synthetic enterprise test matrix with {count} discrete profiles...")
    
    vendors = ["Acme Corp", "Delta Labs", "Vertex Media", "Global Logistics", "Titan Heavy Industries"]
    valid_pos = ["PO-9901", "PO-9902", "PO-9903"]
    amounts = {
        "PO-9901": 1500.00,
        "PO-9902": 420.50,
        "PO-9903": 8900.00
    }
    
    test_suite = []
    
    for i in range(1, count + 1):
        case_type = random.choice(["valid", "mismatch", "invalid_po"])
        vendor = random.choice(vendors)
        
        if case_type == "valid":
            po = random.choice(valid_pos)
            amt = amounts[po]
            text = f"Urgent request: Process transfer authorization to {vendor} for order registration {po}. Total fee is {amt} USD."
            expected_routing = "approve"
            expected_reconciled = True
        elif case_type == "mismatch":
            po = random.choice(valid_pos)
            amt = amounts[po] + round(random.uniform(10.0, 500.0), 2) # Inject variance deviation
            text = f"Inbound invoice check: {vendor} has billed an amount of {amt} against contract document {po}. Verify ledger record."
            expected_routing = "flag_discrepancy"
            expected_reconciled = False
        else:
            po = f"PO-{random.randint(1000, 8800)}" # Token anomaly PO reference
            amt = round(random.uniform(50.0, 5000.0), 2)
            text = f"Notice of transaction: settle out-of-network balance of {amt} to vendor {vendor} tracking back to baseline clearance id {po}."
            expected_routing = "flag_discrepancy"
            expected_reconciled = False
            
        test_suite.append({
            "id": i,
            "text": text,
            "expected_routing": expected_routing,
            "expected_reconciled": expected_reconciled
        })
        
    with open(output_path, 'w') as f:
        json.dump(test_suite, f, indent=2)
    print(f" -> Large-scale validation ledger saved successfully to: {output_path}\n")

if __name__ == "__main__":
    generate_enterprise_test_suite("evaluation/test_bench_large.json", 1000)
