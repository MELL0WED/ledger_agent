from app.schema import AgentState
from app.database.pg_client import query_postgres_erp
from app.database.qdrant_client import search_compliance_vectors

def run_audit_agent(state: AgentState) -> dict:
    """
    Node 2: Verify transactions against PostgreSQL ERP ledger and Qdrant compliance vectors.
    """
    data = state.extracted_data
    if not data:
        return {"is_reconciled": False, "routing_path": "error_fallback"}
        
    po = data.get("po_number")
    vendor = data.get("vendor_name")
    invoice_amount = float(data.get("amount", 0.0))
    
    # 1. Direct Relational SQL query against PostgreSQL container
    pg_record = query_postgres_erp(po)
    if not pg_record:
        return {
            "is_reconciled": False,
            "routing_path": "flag_discrepancy",
            "resolution_log": f"Audit Failed: PO '{po}' not registered in PostgreSQL ERP system."
        }
        
    # 2. Semantic lookup across Qdrant Vector container
    compliance_memos = search_compliance_vectors(vendor, limit=1)
    compliance_context = compliance_memos[0] if compliance_memos else ""
    
    # 3. Dynamic Audit Rules Check
    authorized_amount = float(pg_record["authorized_amount"])
    variance = abs(authorized_amount - invoice_amount)
    
    # If the policy allows variance, check limits; otherwise enforce absolute equality
    if "variance" in compliance_context.lower() and "5%" in compliance_context.lower():
        max_allowed_variance = authorized_amount * 0.05
        if variance > max_allowed_variance:
            return {
                "is_reconciled": False,
                "routing_path": "flag_discrepancy",
                "resolution_log": f"Audit Failed: 5% Variance Exceeded. Allowed: {max_allowed_variance}, Found: {variance}."
            }
    elif variance > 0.01:
        return {
            "is_reconciled": False,
            "routing_path": "flag_discrepancy",
            "resolution_log": f"Audit Failed: Amount mismatch in Postgres. ERP: {authorized_amount}, Invoice: {invoice_amount}."
        }
        
    return {
        "is_reconciled": True,
        "routing_path": "approve",
        "resolution_log": f"Audit Success: Matches Postgres records and passes Qdrant context rules safely."
    }
