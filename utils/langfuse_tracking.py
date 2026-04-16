"""
Langfuse Tracking System for Reply Mirror Challenge
OBRIGATÓRIO: Todos os custos são rastreados via Langfuse session IDs
"""

import os
import ulid
from langfuse import Langfuse, observe
from langfuse.langchain import CallbackHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Langfuse client
langfuse_client = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://challenges.reply.com/langfuse")
)


def generate_session_id():
    """
    Generate unique session ID in format: {TEAM_NAME}-{ULID}
    
    IMPORTANTE: Session ID NÃO pode conter espaços - substituir por hífens
    
    Returns:
        str: Unique session ID
    """
    team = os.getenv("TEAM_NAME", "default-team").replace(" ", "-")
    session_id = f"{team}-{ulid.new().str}"
    return session_id


def get_langfuse_handler():
    """
    Create Langfuse callback handler for LangChain
    
    Returns:
        CallbackHandler: Langfuse callback handler instance
    """
    return CallbackHandler()


@observe()
def run_llm_call(session_id, model, prompt):
    """
    Run LangChain invocation with automatic Langfuse tracking
    
    Este padrão é OBRIGATÓRIO para tracking de custos:
    - @observe() decorator cria trace
    - CallbackHandler() captura tokens e custos
    - metadata.langfuse_session_id agrupa chamadas
    
    Args:
        session_id (str): Unique session identifier
        model: LangChain model instance
        prompt (str): User prompt
        
    Returns:
        str: Model response content
    """
    from langchain_core.messages import HumanMessage
    
    # Create handler inside decorated function (automatically attaches to current trace)
    langfuse_handler = CallbackHandler()
    messages = [HumanMessage(content=prompt)]
    
    # Invoke with tracking
    response = model.invoke(
        messages,
        config={
            "callbacks": [langfuse_handler],
            "metadata": {"langfuse_session_id": session_id}
        }
    )
    
    return response.content


@observe()
def run_agent_call(session_id, agent, input_data):
    """
    Run agent with Langfuse tracking

    Args:
        session_id (str): Unique session identifier
        agent: Agent instance
        input_data (dict): Input data for agent

    Returns:
        Agent response
    """
    import time
    start_time = time.time()

    langfuse_handler = CallbackHandler()

    response = agent.invoke(
        input_data,
        config={
            "callbacks": [langfuse_handler],
            "metadata": {"langfuse_session_id": session_id}
        }
    )

    # Ensure minimum latency for Langfuse
    elapsed = time.time() - start_time
    if elapsed < 0.001:  # Less than 1ms
        time.sleep(0.001 - elapsed)

    return response


def flush_langfuse():
    """
    Flush Langfuse client to ensure all traces are sent
    
    IMPORTANTE: Sempre chamar após sessões para garantir envio de traces
    """
    langfuse_client.flush()
    print("✓ Langfuse traces flushed")


def create_span_with_minimum_latency(name, **kwargs):
    """
    Create a Langfuse span with guaranteed minimum latency > 0

    Args:
        name (str): Span name
        **kwargs: Additional keyword arguments for start_span

    Returns:
        Span object
    """
    import time

    span = langfuse_client.start_span(name=name, **kwargs)

    # Ensure minimum latency
    time.sleep(0.001)  # 1ms minimum

    return span


def end_span_with_flush(span):
    """
    End a span and flush to ensure it's sent to Langfuse

    Args:
        span: Langfuse span object
    """
    span.end()
    langfuse_client.flush()
