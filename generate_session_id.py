#!/usr/bin/env python3
"""
Generate a new Langfuse session ID for Reply Challenge submission

Usage:
    python generate_session_id.py [level]
    
Example:
    python generate_session_id.py 2  # Generate ID for level 2
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import ULID
try:
    import ulid
except ImportError:
    print("❌ Error: ulid module not installed")
    print("   Run: pip install python-ulid")
    sys.exit(1)


def generate_session_id_for_level(level=None):
    """
    Generate unique session ID for a specific level
    
    Format: {TEAM_NAME}-level{N}-{ULID}
    
    Args:
        level (int, optional): Challenge level (1-5)
        
    Returns:
        str: Unique session ID
    """
    team = os.getenv("TEAM_NAME", "default-team").replace(" ", "-")
    ulid_str = ulid.new().str
    
    if level:
        session_id = f"{team}-level{level}-{ulid_str}"
    else:
        session_id = f"{team}-{ulid_str}"
    
    return session_id


def main():
    """Main entry point"""
    print("=" * 70)
    print("Langfuse Session ID Generator - Reply Challenge")
    print("=" * 70)
    
    # Get level from command line argument
    level = None
    if len(sys.argv) > 1:
        try:
            level = int(sys.argv[1])
            if level < 1 or level > 5:
                print(f"⚠️  Warning: Level {level} is outside range 1-5")
        except ValueError:
            print(f"❌ Error: Invalid level '{sys.argv[1]}' - must be a number")
            sys.exit(1)
    
    # Get team name
    team_name = os.getenv("TEAM_NAME", "default-team")
    print(f"\n📋 Team: {team_name}")
    
    if level:
        print(f"🎯 Level: {level}")
    
    # Generate session ID
    session_id = generate_session_id_for_level(level)
    
    print("\n" + "=" * 70)
    print("✅ NEW SESSION ID GENERATED")
    print("=" * 70)
    print(f"\n{session_id}\n")
    print("=" * 70)
    
    # Validation checks
    print("\n✓ Validation:")
    print(f"  • No spaces: {'✅' if ' ' not in session_id else '❌'}")
    print(f"  • Contains team name: {'✅' if team_name.replace(' ', '-') in session_id else '❌'}")
    print(f"  • Contains ULID: {'✅' if len(session_id.split('-')[-1]) == 26 else '❌'}")
    
    if level:
        print(f"  • Contains level {level}: {'✅' if f'level{level}' in session_id else '❌'}")
    
    print("\n💡 Usage:")
    print(f"  1. Copy the session ID above")
    print(f"  2. Use it when submitting your level {level if level else 'X'} output to the platform")
    print(f"  3. This ID is unique and can only be used ONCE")
    print(f"  4. Generate a new ID for each new submission")
    
    print("\n⚠️  IMPORTANT:")
    print("  • Each submission requires a NEW unique session ID")
    print("  • Do not reuse session IDs from previous submissions")
    print("  • Session IDs track your LLM usage and costs")
    
    print("\n" + "=" * 70)
    
    # Save to file for easy reference
    output_file = f"session_id_level{level}.txt" if level else "session_id.txt"
    with open(output_file, 'w') as f:
        f.write(session_id)
    
    print(f"\n💾 Session ID saved to: {output_file}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
