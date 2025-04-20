#!/usr/bin/env python
"""
Detailed test runner for the conversation extractor with human-readable output
"""
import os
import sys
import inspect
import pytest

# Add parent directory to path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
END = "\033[0m"


def print_header(text):
    """Print a formatted header."""
    width = 80
    print("\n" + "=" * width)
    print(f"{BOLD}{BLUE}{text.center(width)}{END}")
    print("=" * width)


def print_subheader(text):
    """Print a formatted subheader."""
    print(f"\n{BOLD}{YELLOW}{text}{END}")
    print("-" * len(text))


def print_feature(text):
    """Print a formatted feature name."""
    print(f"\n{BOLD}{UNDERLINE}{text}{END}")


def print_success(text):
    """Print a success message."""
    print(f"{GREEN}✓ {text}{END}")


def print_failure(text):
    """Print a failure message."""
    print(f"{RED}✗ {text}{END}")


def print_info(text):
    """Print an info message."""
    print(f"{BLUE}ℹ {text}{END}")


def get_sample_conversation():
    """Get the sample conversation text."""
    return """USER: Hello there
ASSISTANT: Hi! How can I help you today?
USER: I'm looking for information about Python
ASSISTANT: Python is a versatile programming language.
It's great for beginners and experts alike.
USER: What about data analysis?
ASSISTANT: Python is excellent for data analysis.
Libraries like pandas and numpy are very popular.
USER: Thanks for the information
ASSISTANT: You're welcome! Let me know if you have more questions."""


def run_detailed_tests():
    """Run detailed tests with human-readable output."""
    print_header("CONVERSATION EXTRACTOR DETAILED TEST REPORT")
    
    # Import the test module
    from tests import test_conversation_extractor_verbose
    
    # Get the sample conversation
    conversation_text = get_sample_conversation()
    
    # Map test functions to their names and descriptions
    tests = [
        (test_conversation_extractor_verbose.test_load_conversation, "Loading conversation from file"),
        (test_conversation_extractor_verbose.test_load_conversation_nonexistent_file, "Error handling for nonexistent files"),
        (test_conversation_extractor_verbose.test_extract_context_single_keyword, "Extracting context for a single keyword"),
        (test_conversation_extractor_verbose.test_extract_context_multiple_keywords, "Extracting context for multiple keywords"),
        (test_conversation_extractor_verbose.test_extract_context_no_matches, "Handling no matches"),
        (test_conversation_extractor_verbose.test_extract_context_case_insensitive, "Case-insensitive matching"),
        (test_conversation_extractor_verbose.test_extract_context_boundaries, "Handling text boundaries"),
        (test_conversation_extractor_verbose.test_extract_context_varying_context_size, "Different context sizes"),
        (test_conversation_extractor_verbose.test_real_file_integration, "End-to-end integration")
    ]
    
    # Display the sample conversation
    print_subheader("SAMPLE CONVERSATION")
    print(conversation_text)
    
    # Display the features being tested
    print_subheader("FEATURES BEING TESTED")
    
    for i, (test_func, description) in enumerate(tests, 1):
        # Get the docstring
        doc = test_func.__doc__ or ""
        
        # Extract the feature description (everything after "FEATURE:")
        feature_desc = None
        rest_of_doc = ""
        for line in doc.split("\n"):
            if "FEATURE:" in line:
                feature_desc = line.split("FEATURE:")[1].strip()
                doc_lines = doc.split("\n")
                start_idx = doc_lines.index(line) + 1
                rest_lines = [l.strip() for l in doc_lines[start_idx:] if l.strip()]
                if rest_lines:
                    rest_of_doc = "\n   ".join(rest_lines)
                break
        
        if feature_desc:
            print(f"{i}. {BOLD}{feature_desc}{END}")
            if rest_of_doc:
                print(f"   {rest_of_doc}")
            print()
    
    # Run the actual tests
    print_subheader("RUNNING TESTS")
    print("Running pytest with verbose output...\n")
    
    # Determine the output directory for HTML report
    output_dir = os.path.dirname(os.path.abspath(__file__))
    html_report = os.path.join(output_dir, "test_report.html")
    
    # Run the tests
    result = pytest.main(["-v", "--html=" + html_report, "tests/test_conversation_extractor_verbose.py"])
    
    # Print summary
    print_header("SUMMARY")
    if result == 0:
        print(f"{GREEN}All tests passed!{END}")
        print(f"HTML report saved to: {html_report}")
    else:
        print(f"{RED}Some tests failed. See above for details.{END}")
    
    return result


if __name__ == "__main__":
    sys.exit(run_detailed_tests())
