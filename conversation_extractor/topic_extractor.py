"""
Topic Extractor Module

Extract and group conversation topics based on keywords.
"""
from collections import defaultdict
from .extractor import extract_context

# Define topic categories and their associated keywords
DEFAULT_TOPIC_CATEGORIES = {
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


def extract_topics(conversation_text, topic_categories=None, context_lines=3):
    """
    Extract and group conversation topics based on predefined categories.
    
    Args:
        conversation_text: The conversation text to analyze
        topic_categories: Dictionary mapping topic categories to lists of keywords
                         (defaults to DEFAULT_TOPIC_CATEGORIES if None)
        context_lines: Number of context lines to include
        
    Returns:
        Dictionary mapping topic categories to their extracted contexts
    """
    # Use default categories if none provided
    if topic_categories is None:
        topic_categories = DEFAULT_TOPIC_CATEGORIES
    
    # Initialize results dictionary
    topic_results = defaultdict(list)
    
    # Process each topic category
    for category, keywords in topic_categories.items():
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
