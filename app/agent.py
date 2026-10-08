import os
import hashlib
from dotenv import load_dotenv
from groq import Groq
from langgraph.graph import StateGraph, END

from app.schema import AgentState
from app.database.redis_cache import get_semantic_cache, set_semantic_cache
from app.agents.parser_agent import run_parser_agent
from app.agents.audit_agent import run_audit_agent

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def orchestrate_parser_node(state: AgentState) -> dict:
    """
    Entry Coordinator: Intercepts workflow with Redis semantic lookup before invoking Groq.
    """
    # Create an atomic structural fingerprint hash out of the raw input text string
    string_hash = hashlib.md5(state.raw_input.strip().lower().encode('utf-8')).hexdigest()
    
    # Check the Redis cache cluster container
    cached_payload = get_semantic_cache(string_hash)
    if cached_payload:
        print(" -> [REDIS CACHE HIT] Bypassed core LLM parsing inference successfully.")
        return cached_payload
        
    # Cache Miss: Execute deep-learning processing
    print(" -> [REDIS CACHE MISS] Executing gpt-oss-20b structural parsing pipeline...")
    agent_output = run_parser_agent(state, client)
    
    # Store result into cache if parsing succeeded
    if agent_output.get("extraction_error") is None:
        set_semantic_cache(string_hash, agent_output, ttl=3600)
        
    return agent_output

def orchestrate_audit_node(state: AgentState) -> dict:
    """Invokes our distributed verification node logic across Postgres & Qdrant."""
    return run_audit_agent(state)

def evaluate_routing_direction(state: AgentState) -> str:
    """Conditional routing evaluator."""
    return state.routing_path
def orchestrate_parser_node(state: AgentState) -> dict:
    """
    Entry Coordinator: Intercepts workflow with Redis semantic lookup before invoking Groq.
    """
    # Create an atomic structural fingerprint hash out of the raw input text string
    string_hash = hashlib.md5(state.raw_input.strip().lower().encode('utf-8')).hexdigest()
    
    # Check the Redis cache cluster container
    cached_payload = get_semantic_cache(string_hash)
    
    # SAFETY REFINEMENT: Only trigger hit if the cached entry holds validated extracted elements
    if cached_payload and cached_payload.get("extracted_data") is not None:
        print(" -> [REDIS CACHE HIT] Bypassed core LLM parsing inference successfully.")
        return cached_payload
        
    # Cache Miss / Fallback Recovery: Execute deep-learning processing
    print(" -> [REDIS CACHE MISS] Executing gpt-oss-20b structural parsing pipeline...")
    agent_output = run_parser_agent(state, client)
    
    # Store result into cache ONLY if parsing succeeded and data object is intact
    if agent_output.get("extraction_error") is None and agent_output.get("extracted_data") is not None:
        set_semantic_cache(string_hash, agent_output, ttl=3600)
        
    return agent_output


# Compile State Machine Infrastructure Blueprint Graph Topology
workflow = StateGraph(AgentState)

workflow.add_node("extract_invoice", orchestrate_parser_node)
workflow.add_node("reconcile_ledger", orchestrate_audit_node)

workflow.set_entry_point("extract_invoice")

workflow.add_conditional_edges(
    "extract_invoice",
    evaluate_routing_direction,
    {"audit": "reconcile_ledger", "error_fallback": END}
)

workflow.add_conditional_edges(
    "reconcile_ledger",
    evaluate_routing_direction,
    {"approve": END, "flag_discrepancy": END, "error_fallback": END}
)

app_graph = workflow.compile()
