#!/usr/bin/env python3
"""
Generate a new Langfuse session ID and send it to the dashboard
"""

import os
import sys
from dotenv import load_dotenv
from datetime import datetime
from utils.langfuse_tracking import generate_session_id, langfuse_client, create_span_with_minimum_latency, end_span_with_flush

# Load environment variables
load_dotenv()

def create_and_send_session():
    """Generate session ID and register it with Langfuse"""
    
    # Generate new session ID
    session_id = generate_session_id()
    print(f"\n{'='*60}")
    print(f"NEW LANGFUSE SESSION GENERATED")
    print(f"{'='*60}")
    print(f"Session ID: {session_id}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    # Create session in Langfuse
    try:
        # Create a span with session metadata and guaranteed minimum latency
        span = create_span_with_minimum_latency(
            name="session_initialization",
            metadata={
                "langfuse_session_id": session_id,
                "session_created_at": datetime.now().isoformat(),
                "type": "new_session_generated"
            }
        )

        # End the span and flush
        end_span_with_flush(span)

        print(f"Trace ID: {span.trace_id}")
        
        # Get dashboard URL
        host = os.getenv("LANGFUSE_HOST", "https://challenges.reply.com/langfuse")
        dashboard_url = f"{host}/sessions/{session_id}"
        
        print(f"\n{'='*60}")
        print(f"LANGFUSE DASHBOARD")
        print(f"{'='*60}")
        print(f"Dashboard URL: {dashboard_url}")
        print(f"\nYou can now view this session's metrics, costs, and traces")
        print(f"in the Langfuse dashboard.")
        
        # Save session info
        session_info = {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "dashboard_url": dashboard_url
        }
        
        print(f"\n{'='*60}")
        print(f"Session information saved and ready to use!")
        print(f"{'='*60}\n")
        
        return session_info
        
    except Exception as e:
        print(f"✗ Error registering session: {str(e)}")
        print(f"Make sure LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY are set")
        sys.exit(1)

if __name__ == "__main__":
    create_and_send_session()
