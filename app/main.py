from app.agent import app_graph
from app.schema import AgentState

def execute_ledger_agent(unstructured_text: str) -> dict:
    """
    Invokes the compiled agent graph with a clean unstructured entry point.
    """
    initial_state = AgentState(raw_input=unstructured_text)
    final_output_state = app_graph.invoke(initial_state)
    return final_output_state
