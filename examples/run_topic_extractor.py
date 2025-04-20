#!/usr/bin/env python
"""
Script to demonstrate the topic extraction functionality
"""
import os
import sys
import pathlib

# Add parent directory to path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from conversation_extractor import (
    load_conversation, 
    extract_topics, 
    print_topic_results
)


def main():
    """Main function to demonstrate the topic extraction."""
    # Use the sample file from the test data directory
    sample_file = os.path.join(os.path.dirname(__file__), "..", "tests", "data", "coding_buddy_conversation.txt")
    if not os.path.exists(sample_file):
        print(f"Sample file '{sample_file}' not found. Please create it first.")
        return 1
    
    # Load the conversation
    conversation = load_conversation(sample_file)
    if not conversation:
        return 1
    
    print(f"Loaded conversation from {sample_file}")
    print(f"({len(conversation)} characters, {len(conversation.split('\\n'))} lines)")
    
    # Extract topics with 2 lines of context
    context_lines = 2
    print(f"Extracting topics with {context_lines} lines of context...")
    
    # Extract and print topics
    topic_results = extract_topics(conversation, context_lines=context_lines)
    print_topic_results(topic_results)
    
    # Print summary
    print("\nTOPIC SUMMARY:")
    print("-" * 40)
    for category, matches in topic_results.items():
        unique_contexts = set()
        for _, _, context in matches:
            unique_contexts.add(tuple(context))
        print(f"{category}: {len(unique_contexts)} unique contexts")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
