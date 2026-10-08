from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

# This enforces that the LLM extracts EXACT data types from messy input strings
class ExtractedInvoice(BaseModel):
    vendor_name: str = Field(description="Cleaned, standardized name of the vendor/merchant.")
    amount: float = Field(description="Total monetary value extracted as a float numeric.")
    po_number: str = Field(description="The unique Purchase Order identifier string. Use 'UNKNOWN' if missing.")

# This represents the internal running state memory of our LangGraph agent
class AgentState(BaseModel):
    raw_input: str = Field(description="The dirty inbound raw ledger entry text.")
    extracted_data: Optional[Dict[str, Any]] = None
    extraction_error: Optional[str] = None
    is_reconciled: bool = False
    routing_path: str = "init"
    resolution_log: str = ""
