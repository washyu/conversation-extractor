#!/usr/bin/env python
"""
Simple script to run the conversation extractor.
"""
import os
import sys
import pathlib

# Add parent directory to path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from conversation_extractor import load_conversation, extract_context, print_results


def main():
    """Interactive main function."""
    # Check if sample file exists
    sample_file = os.path.join(os.path.dirname(__file__), "sample_conversation.txt")
    if not os.path.exists(sample_file):
        # Try to use the test data file if available
        test_data_file = os.path.join(os.path.dirname(__file__), "..", "tests", "data", "coding_buddy_conversation.txt")
        if os.path.exists(test_data_file):
            sample_file = test_data_file
        else:
            print(f"Sample file not found. Please create a file named 'sample_conversation.txt' in the examples directory.")
            return 1
    
    # Load the conversation
    conversation = load_conversation(sample_file)
    if not conversation:
        return 1
    
    print(f"Loaded conversation from {sample_file}")
    print(f"({len(conversation)} characters, {len(conversation.split('\\n'))} lines)")
    
    # Get keywords from user
    keywords_input = input("Enter keywords to search for (comma-separated): ")
    keywords = [k.strip() for k in keywords_input.split(',') if k.strip()]
    
    if not keywords:
        print("No valid keywords provided.")
        return 1
    
    # Get context lines
    try:
        context_lines = int(input("Enter number of context lines (default: 3): ") or "3")
    except ValueError:
        context_lines = 3
        print("Invalid input, using default value of 3 context lines.")
    
    # Extract and print context
    results = extract_context(conversation, keywords, context_lines)
    print_results(results)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
