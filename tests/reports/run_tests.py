#!/usr/bin/env python
"""
Custom test runner for the conversation extractor with human-readable output
"""
import os
import sys
import pytest
import time
from io import StringIO
from contextlib import redirect_stdout

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


def run_tests():
    """Run the tests and display human-readable output."""
    print_header("CONVERSATION EXTRACTOR TEST SUITE")
    
    # Run the tests with output visible
    print("\nRunning tests with detailed logging...\n")
    
    # Determine the output directory for HTML report
    output_dir = os.path.dirname(os.path.abspath(__file__))
    html_report = os.path.join(output_dir, "test_report.html")
    
    result = pytest.main(["-v", "-s", "--html=" + html_report, "tests/test_conversation_extractor_verbose.py"])
    
    # Capture the test output for parsing
    buffer = StringIO()
    with redirect_stdout(buffer):
        # Run the tests again silently to parse results
        pytest.main(["-v", "tests/test_conversation_extractor_verbose.py"])
    
    # Parse the output
    output = buffer.getvalue()
    lines = output.split("\n")
    
    # Extract test results
    test_results = []
    current_test = None
    
    for line in lines:
        if "::test_" in line:
            # Extract test name and result
            parts = line.split("::")
            if len(parts) >= 2:
                test_name = parts[1].split(" ")[0]
                result = "PASSED" if "PASSED" in line else "FAILED"
                test_results.append((test_name, result))
    
    # Import the test module to get docstrings
    from tests import test_conversation_extractor_verbose
    
    # Map test functions to their names
    test_functions = {
        "test_load_conversation": test_conversation_extractor_verbose.test_load_conversation,
        "test_load_conversation_nonexistent_file": test_conversation_extractor_verbose.test_load_conversation_nonexistent_file,
        "test_extract_context_single_keyword": test_conversation_extractor_verbose.test_extract_context_single_keyword,
        "test_extract_context_multiple_keywords": test_conversation_extractor_verbose.test_extract_context_multiple_keywords,
        "test_extract_context_no_matches": test_conversation_extractor_verbose.test_extract_context_no_matches,
        "test_extract_context_case_insensitive": test_conversation_extractor_verbose.test_extract_context_case_insensitive,
        "test_extract_context_boundaries": test_conversation_extractor_verbose.test_extract_context_boundaries,
        "test_extract_context_varying_context_size": test_conversation_extractor_verbose.test_extract_context_varying_context_size,
        "test_real_file_integration": test_conversation_extractor_verbose.test_real_file_integration
    }
    
    # Display results in a human-readable format
    print_header("TEST RESULTS")
    
    passed = 0
    failed = 0
    
    for test_name, result in test_results:
        # Get the docstring
        doc = test_functions.get(test_name).__doc__ or ""
        
        # Extract the feature name (first line after "FEATURE:")
        feature = None
        for line in doc.split("\n"):
            if "FEATURE:" in line:
                feature = line.split("FEATURE:")[1].strip()
                break
        
        if feature:
            print_feature(feature)
        
        # Print the test result
        if result == "PASSED":
            print_success(f"{test_name} - {feature}")
            passed += 1
        else:
            print_failure(f"{test_name} - {feature}")
            failed += 1
    
    # Print summary
    print_header("SUMMARY")
    print(f"Total tests: {passed + failed}")
    print(f"{GREEN}Passed: {passed}{END}")
    print(f"{RED}Failed: {failed}{END}")
    print(f"HTML report saved to: {html_report}")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_tests())
