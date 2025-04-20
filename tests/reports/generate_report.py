"""
Generate a detailed test report for the conversation extractor
"""
import os
import inspect
import sys
import importlib
from pathlib import Path

# Add parent directory to path so we can import test modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


def generate_test_report(output_file=None):
    """
    Generate a detailed report of all tests and what they're testing.
    
    Args:
        output_file: Optional file path to save the report to
    """
    # Import test modules
    from tests import test_conversation_extractor
    from tests import test_topic_extractor
    from tests import test_topic_extraction
    from tests import test_coding_buddy
    
    # Get all test modules
    test_modules = [
        test_conversation_extractor,
        test_topic_extractor,
        test_topic_extraction,
        test_coding_buddy
    ]
    
    # Prepare output
    report_lines = []
    
    def add_line(line=""):
        if output_file:
            report_lines.append(line)
        print(line)
    
    add_line("\n" + "="*80)
    add_line("CONVERSATION EXTRACTOR TEST REPORT")
    add_line("="*80)
    
    total_tests = 0
    
    # Process each module
    for module in test_modules:
        module_name = module.__name__.split('.')[-1]
        add_line(f"\n\nMODULE: {module_name}")
        add_line("-" * (len(module_name) + 8))
        
        # Get all test functions from the module
        test_functions = [obj for name, obj in inspect.getmembers(module) 
                         if name.startswith("test_") and callable(obj)]
        
        total_tests += len(test_functions)
        
        for i, test_func in enumerate(test_functions, 1):
            # Get the function name and docstring
            name = test_func.__name__
            doc = test_func.__doc__ or "No description available"
            
            # Extract feature description
            feature_desc = None
            for line in doc.split("\n"):
                if "FEATURE:" in line:
                    feature_desc = line.split("FEATURE:")[1].strip()
                    break
            
            # Get the source code
            try:
                source = inspect.getsource(test_func)
                # Extract assertions
                assertions = [line.strip() for line in source.split("\n") 
                             if "assert" in line and not line.strip().startswith("#")]
            except Exception:
                assertions = ["Could not extract assertions"]
            
            add_line(f"\n{i}. {name}")
            add_line("-" * (len(name) + 3))
            if feature_desc:
                add_line(f"Feature: {feature_desc}")
            add_line(f"Description: {doc.strip()}")
            add_line("Assertions:")
            for j, assertion in enumerate(assertions, 1):
                add_line(f"  {j}. {assertion.strip()}")
    
    add_line("\n" + "="*80)
    add_line(f"Total tests: {total_tests}")
    add_line("="*80 + "\n")
    
    # Save to file if requested
    if output_file:
        with open(output_file, 'w') as f:
            f.write('\n'.join(report_lines))
        print(f"Report saved to {output_file}")


if __name__ == "__main__":
    # Determine output file path
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, "test_report.txt")
    
    generate_test_report(output_file)
