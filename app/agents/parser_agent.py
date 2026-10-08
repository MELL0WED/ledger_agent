import json
from groq import Groq
from app.schema import AgentState, ExtractedInvoice
from tenacity import retry, stop_after_attempt, wait_random_exponential

# Retries the function if an API exception hits, stopping after 5 attempts with randomized backoff delays
@retry(wait=wait_random_exponential(min=2, max=10), stop=stop_after_attempt(5))
def call_groq_with_retry(client: Groq, system_prompt: str, user_input: str):
    """Encapsulates the raw HTTP network barrier call inside an exponential backoff loop."""
    return client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Parse this invoice payload: {user_input}"}
        ],
        response_format={
            "type": "json_object",
            "schema": ExtractedInvoice.model_json_schema()
        },
        temperature=0.0
    )

def run_parser_agent(state: AgentState, client: Groq) -> dict:
    """
    Node 1: Extract unstructured financial inputs into clean Pydantic schemas.
    Harden against upstream HTTP 429 / Rate Limit degradation loops using Tenacity.
    """
    system_prompt = (
        "You are an elite B2B accounting system parsing agent. "
        "Your sole task is to extract vendor_name, amount, and po_number from the user payload. "
        "You must output a structured JSON object matching the exact schema definition provided."
    )
    
    try:
        # Trigger the network-resilient wrapper execution loop
        response = call_groq_with_retry(client, system_prompt, state.raw_input)
        
        raw_content = response.choices[0].message.content
        parsed_dict = json.loads(raw_content)
        
        # Runtime schema validation guarantee
        validated_data = ExtractedInvoice(**parsed_dict)
        
        return {
            "extracted_data": validated_data.model_dump(),
            "extraction_error": None,
            "routing_path": "audit"
        }
    except Exception as e:
        return {
            "extraction_error": f"Rate-limit or validation collapse: {str(e)}",
            "routing_path": "error_fallback"
        }
