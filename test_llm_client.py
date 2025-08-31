#!/usr/bin/env python3
"""
Simple test script for llm_client.py
"""

from llm_client import call_model


def main():
    """Simple test with one prompt"""
    print("Testing LLM Client...")
    
    try:
        response = call_model("Hello! How are you today?")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
