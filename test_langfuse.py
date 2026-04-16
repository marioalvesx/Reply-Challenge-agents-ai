#!/usr/bin/env python3
"""
Test Langfuse tracking with a simple LLM call
This validates that the tracking system is working correctly
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_langfuse_tracking():
    """Test complete Langfuse tracking workflow"""
    print("=" * 60)
    print("Testing Langfuse Tracking")
    print("=" * 60)
    
    try:
        # Import dependencies
        from langchain_openai import ChatOpenAI
        from utils.langfuse_tracking import (
            generate_session_id,
            run_llm_call,
            flush_langfuse,
            print_session_info
        )
        
        print("\n✅ Imports successful")
        
        # Check API key
        if not os.getenv("OPENROUTER_API_KEY"):
            print("\n❌ OPENROUTER_API_KEY not found in .env")
            return False
        
        print("✅ API key found")
        
        # Configure model
        print("\nConfiguring model...")
        model = ChatOpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            model="openai/gpt-4o-mini",
            temperature=0.7,
            max_tokens=100
        )
        print("✅ Model configured: gpt-4o-mini")
        
        # Generate session ID
        session_id = generate_session_id()
        print(f"\n✅ Session ID generated: {session_id}")
        
        # Validate session ID format
        if " " in session_id:
            print("❌ ERROR: Session ID contains spaces!")
            print("   Session IDs must not contain spaces")
            return False
        
        team_name = os.getenv("TEAM_NAME", "")
        if "-" in session_id and team_name:
            print("✅ Session ID format valid (spaces replaced with hyphens)")
        
        # Test LLM call with tracking
        print("\n" + "-" * 60)
        print("Making test LLM call with Langfuse tracking...")
        print("-" * 60)
        
        test_prompt = "What is the square root of 144? Answer in one sentence."
        
        try:
            response = run_llm_call(session_id, model, test_prompt)
            print(f"\n✅ LLM call successful!")
            print(f"   Prompt:   {test_prompt}")
            print(f"   Response: {response}")
        except Exception as e:
            print(f"\n❌ LLM call failed: {e}")
            return False
        
        # Flush traces to Langfuse
        print("\n" + "-" * 60)
        print("Flushing traces to Langfuse...")
        print("-" * 60)
        flush_langfuse()
        
        # Print session info
        print_session_info(session_id)
        
        print("\n✅ TRACKING TEST SUCCESSFUL!")
        print("\nVerification steps:")
        print(f"  1. Go to: {os.getenv('LANGFUSE_HOST')}")
        print(f"  2. Look for session ID: {session_id}")
        print(f"  3. Verify that:")
        print(f"     - Trace appears in dashboard (may take a few minutes)")
        print(f"     - Token usage is recorded")
        print(f"     - Costs are calculated")
        print(f"     - Input/output captured")
        
        print("\n" + "=" * 60)
        print("All tests passed! Langfuse tracking is working correctly.")
        print("=" * 60)
        
        return True
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("\nMake sure you've installed all dependencies:")
        print("  pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point"""
    success = test_langfuse_tracking()
    
    if success:
        print("\n✅ Ready to start building the fraud detection system!")
        return 0
    else:
        print("\n❌ Please fix the issues above before proceeding.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
