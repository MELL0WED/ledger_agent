import time

# A clean local look-up registry simulating our enterprise system records
LEDGER_ERP_DB = {
    "PO-9901": {"vendor": "Acme Corp", "amount": 1500.00},
    "PO-9902": {"vendor": "Delta Labs", "amount": 420.50},
    "PO-9903": {"vendor": "Vertex Media", "amount": 8900.00}
}

def query_erp_ledger(po_number: str) -> dict:
    """Simulates a low-latency database read operation."""
    # Simulating a real networking/disk IO tick to keep latency measurements true
    time.sleep(0.02) 
    return LEDGER_ERP_DB.get(po_number, {})
