#!/usr/bin/env python
"""
Script to demonstrate the dynamic keyword generation functionality
"""
import os
import sys
import pathlib

# Add parent directory to path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from conversation_extractor import (
    load_conversation,
    extract_topics,
    print_topic_results,
    generate_dynamic_keywords,
    KeywordTracker
)


def main():
    """Main function to demonstrate dynamic keyword generation."""
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
    
    # Generate dynamic keywords
    print("\nGenerating dynamic keywords...")
    keywords = generate_dynamic_keywords(conversation)
    
    print(f"\nTop {len(keywords)} dynamic keywords:")
    print("-" * 40)
    for i, keyword in enumerate(keywords, 1):
        print(f"{i}. {keyword}")
    
    # Extract topics with dynamic keywords
    print("\nExtracting topics with dynamic keywords...")
    topic_results = extract_topics(conversation, enable_dynamic=True)
    
    # Print only the dynamic topics
    if "Dynamic Topics" in topic_results:
        print("\nDYNAMIC TOPICS:")
        print("=" * 80)
        
        # Group by matched line to avoid duplicates
        unique_contexts = {}
        for keyword, matched_line, context in topic_results["Dynamic Topics"]:
            # Use the context as the key to avoid duplicates
            context_key = "\n".join(context)
            if context_key not in unique_contexts:
                unique_contexts[context_key] = (keyword, matched_line, context)
        
        # Print unique contexts
        for i, (keyword, matched_line, context) in enumerate(unique_contexts.values(), 1):
            print(f"\nMatch #{i} (matched keyword: '{keyword}'):")
            print(f"{'-'*40}")
            for ctx_line in context:
                # Highlight the matched line
                if ctx_line == matched_line:
                    print(f">>> {ctx_line}")
                else:
                    print(f"    {ctx_line}")
            print()
    else:
        print("\nNo dynamic topics found.")
    
    # Create a keyword tracker
    print("\nTracking keyword importance...")
    tracker = KeywordTracker()
    
    # Update keywords based on the dynamic keywords
    for keyword in keywords[:10]:  # Use top 10 keywords
        tracker.update_keyword(keyword)
    
    # Print the top keywords by importance
    top_keywords = tracker.get_top_keywords()
    print("\nTop keywords by importance:")
    print("-" * 40)
    for i, (keyword, importance) in enumerate(top_keywords, 1):
        print(f"{i}. {keyword}: {importance:.2f}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
