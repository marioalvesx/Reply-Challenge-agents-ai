#!/usr/bin/env python3
"""
Test a specific session ID with Langfuse
Verifies that a session ID can successfully track LLM calls
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()


def test_session_id(session_id):
    """
    Test a specific session ID by making a tracked LLM call
    
    Args:
        session_id (str): Session ID to test
    """
    print("=" * 70)
    print(f"Testing Session ID: {session_id}")
    print("=" * 70)
    
    try:
        from langchain_openai import ChatOpenAI
        from utils.langfuse_tracking import run_llm_call, flush_langfuse
        
        # Configure model
        model = ChatOpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            model="openai/gpt-4o-mini",
            temperature=0.7,
            max_tokens=50
        )
        
        # Make a simple test call
        test_prompt = "Say 'Session ID test successful!' in one sentence."
        
        print(f"\n📞 Making test LLM call with session ID...")
        response = run_llm_call(session_id, model, test_prompt)
        
        print(f"✅ LLM Response: {response}")
        
        # Flush to Langfuse
        print(f"\n📤 Flushing traces to Langfuse...")
        flush_langfuse()
        
        print("\n" + "=" * 70)
        print("✅ TEST SUCCESSFUL!")
        print("=" * 70)
        print(f"\n🔍 Verify in Langfuse Dashboard:")
        print(f"   URL: {os.getenv('LANGFUSE_HOST')}")
        print(f"   Session ID: {session_id}")
        print(f"\n⏱️  Note: It may take 1-2 minutes for the trace to appear")
        print("=" * 70 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python test_session_id.py <session_id>")
        print("\nExample:")
        print("  python test_session_id.py mario-e-matheus-933e-team-level2-01KPBQ4H7NPA70PQ102811M37S")
        
        # Check if session_id file exists
        if os.path.exists("session_id_level2.txt"):
            with open("session_id_level2.txt", "r") as f:
                saved_id = f.read().strip()
            print(f"\n💡 Found saved session ID: {saved_id}")
            print(f"\n   To test it, run:")
            print(f"   python test_session_id.py {saved_id}")
        
        sys.exit(1)
    
    session_id = sys.argv[1]
    test_session_id(session_id)


if __name__ == "__main__":
    main()
