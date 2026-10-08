from app.main import execute_ledger_agent

sample_invoice = "Hey team, settle bill from Acme Corp for PO-9901. Amount is 1500.00 dollars."
print("Invoking Agent pipeline validation check...")
result = execute_ledger_agent(sample_invoice)

print("\n--- HEALTH CHECK DIAGNOSTICS ---")
print(f"Routing Path Terminated At: {result.get('routing_path')}")
print(f"Is Reconciled: {result.get('is_reconciled')}")
print(f"Resolution Details: {result.get('resolution_log')}")
print(f"Extraction Error Found: {result.get('extraction_error')}")
print(f"Full Returned Keys: {list(result.keys())}")
