#!/usr/bin/env python3
"""
Langfuse Latency Diagnostic and Fix Tool
Helps identify and fix latency validation errors
"""

import os
import sys
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

def diagnose_langfuse_latency():
    """Diagnose potential latency issues in Langfuse tracking"""
    print("=" * 60)
    print("LANGFUSE LATENCY DIAGNOSTIC")
    print("=" * 60)

    try:
        from langfuse import Langfuse
        from utils.langfuse_tracking import langfuse_client

        print("\n✅ Langfuse client initialized")

        # Check if there are any pending traces
        print("\nFlushing any pending traces...")
        langfuse_client.flush()
        print("✅ Traces flushed")

        # Test span creation with proper timing
        print("\nTesting span creation with minimum latency...")

        test_span = langfuse_client.start_span(
            name="latency_test",
            metadata={"test_type": "latency_validation"}
        )

        # Ensure minimum latency
        import time
        time.sleep(0.001)  # 1ms

        test_span.end()
        langfuse_client.flush()

        print("✅ Test span created and ended successfully")
        print(f"   Span ID: {test_span.id}")

        print("\n" + "=" * 60)
        print("DIAGNOSTIC COMPLETE")
        print("=" * 60)
        print("\nRecommendations:")
        print("1. Always use minimum 1ms delay between span start/end")
        print("2. Call langfuse_client.flush() after ending spans")
        print("3. Use the utility functions in langfuse_tracking.py")
        print("4. Avoid creating spans that complete instantly")

        return True

    except Exception as e:
        print(f"\n❌ Error during diagnostic: {e}")
        print("\nTroubleshooting steps:")
        print("1. Check LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY")
        print("2. Verify network connectivity to Langfuse host")
        print("3. Ensure Python packages are up to date")
        return False

if __name__ == "__main__":
    diagnose_langfuse_latency()