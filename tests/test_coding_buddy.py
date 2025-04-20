#!/usr/bin/env python
"""
Test the topic extractor on a natural coding buddy conversation
"""
import os
import sys
import pytest
from conversation_extractor import (
    load_conversation, 
    extract_topics, 
    print_topic_results
)


def test_topic_extraction_on_coding_buddy():
    """
    FEATURE: Topic extraction from natural coding buddy conversation
    
    Test that we can extract and categorize topics from a natural conversation
    that mixes technical questions, ADHD challenges, and best practices.
    """
    # Load the conversation from the test data directory
    sample_file = os.path.join(os.path.dirname(__file__), "data", "coding_buddy_conversation.txt")
    assert os.path.exists(sample_file), f"Sample file '{sample_file}' not found."
    
    conversation = load_conversation(sample_file)
    assert conversation, "Failed to load conversation"
    
    print(f"Loaded conversation ({len(conversation)} characters, {len(conversation.split('\\n'))} lines)")
    
    # Extract topics with 2 lines of context
    context_lines = 2
    print(f"Extracting topics with {context_lines} lines of context...")
    
    # Extract and print topics
    topic_results = extract_topics(conversation, context_lines=context_lines)
    
    # Verify that we found all expected topic categories
    expected_categories = [
        "Python Syntax", 
        "Web Development", 
        "Data Processing", 
        "ADHD & Productivity", 
        "Best Practices", 
        "Debugging"
    ]
    
    for category in expected_categories:
        assert category in topic_results, f"Should find '{category}' category"
        
        # Each category should have at least one match
        matches = topic_results[category]
        assert len(matches) > 0, f"Category '{category}' should have at least one match"
    
    # Print summary
    print("\nTOPIC SUMMARY:")
    print("-" * 40)
    for category, matches in topic_results.items():
        # Count unique contexts
        unique_contexts = set()
        for _, _, context in matches:
            context_key = tuple(context)
            unique_contexts.add(context_key)
        
        print(f"{category}: {len(unique_contexts)} unique contexts")
    
    # Test passes if we get here
    assert True


if __name__ == "__main__":
    pytest.main(["-v", __file__])
