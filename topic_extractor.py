#!/usr/bin/env python
"""
Topic Extractor - Extract and group conversation topics based on keywords
"""
import os
import re
from collections import defaultdict
from conversation_extractor import load_conversation, extract_context, print_results

# Define topic categories and their associated keywords
TOPIC_CATEGORIES = {
    "Python Syntax": [
        "syntax", "list comprehension", "dictionary", "function", "class",
        "variable", "loop", "if statement", "for loop", "while loop",
        "def ", "import", "return", "print(", "=", "==", "+=", "-=", "*=", "/=",
        "[]", "{}", "()", ":", "lambda"
    ],
    "Web Development": [
        "Flask", "FastAPI", "Django", "web", "HTML", "CSS", "JavaScript",
        "frontend", "backend", "API", "REST", "HTTP", "route", "template",
        "static", "request", "response", "server", "client", "browser"
    ],
    "Data Processing": [
        "pandas", "numpy", "data", "CSV", "Excel", "DataFrame", "Series",
        "processing", "analysis", "visualization", "plot", "graph", "chart",
        "statistics", "mean", "median", "standard deviation", "correlation"
    ],
    "ADHD & Productivity": [
        "ADHD", "focus", "distraction", "attention", "productivity",
        "Pomodoro", "timer", "break", "task", "planning", "organization",
        "routine", "habit", "reminder", "notification", "dopamine", "reward"
    ],
    "Best Practices": [
        "best practice", "clean code", "maintainable", "readable", "PEP 8",
        "documentation", "comment", "testing", "debug", "logging", "error handling",
        "version control", "git", "structure", "architecture", "pattern", "design"
    ],
    "Debugging": [
        "debug", "error", "exception", "try", "except", "finally", "raise",
        "traceback", "breakpoint", "pdb", "print debugging", "log", "assert",
        "testing", "unit test", "pytest", "unittest"
    ]
}


def extract_topics(conversation_text, context_lines=3):
    """
    Extract and group conversation topics based on predefined categories.
    
    Args:
        conversation_text: The conversation text to analyze
        context_lines: Number of context lines to include
        
    Returns:
        Dictionary mapping topic categories to their extracted contexts
    """
    # Initialize results dictionary
    topic_results = defaultdict(list)
    
    # Process each topic category
    for category, keywords in TOPIC_CATEGORIES.items():
        # Extract context for all keywords in this category
        results = extract_context(conversation_text, keywords, context_lines)
        
        # If we found matches, add them to the category
        if results:
            for keyword, matches in results.items():
                for matched_line, context in matches:
                    # Add the match to the category results
                    # Include the keyword that matched
                    topic_results[category].append((keyword, matched_line, context))
    
    return topic_results


def print_topic_results(topic_results):
    """
    Print the topic extraction results in a readable format.
    
    Args:
        topic_results: Dictionary mapping topic categories to their extracted contexts
    """
    if not topic_results:
        print("No topics found.")
        return
    
    # Print each topic category
    for category, matches in topic_results.items():
        print(f"\n{'='*80}")
        print(f"TOPIC: {category} - {len(matches)} matches found")
        print(f"{'='*80}")
        
        # Group by matched line to avoid duplicates
        unique_contexts = {}
        for keyword, matched_line, context in matches:
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


def main():
    """Main function to demonstrate the topic extraction."""
    # Check if sample file exists
    sample_file = "sample_mixed_conversation.txt"
    if not os.path.exists(sample_file):
        print(f"Sample file '{sample_file}' not found. Please create it first.")
        return 1
    
    # Load the conversation
    conversation = load_conversation(sample_file)
    if not conversation:
        return 1
    
    print(f"Loaded conversation ({len(conversation)} characters, {len(conversation.split('\\n'))} lines)")
    
    # Extract topics with 2 lines of context
    context_lines = 2
    print(f"Extracting topics with {context_lines} lines of context...")
    
    # Extract and print topics
    topic_results = extract_topics(conversation, context_lines)
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
    exit(main())
