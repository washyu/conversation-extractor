#!/usr/bin/env python
"""
Simple script to view test results locally.
This script runs the tests and opens the HTML report in a browser.
"""
import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def run_tests_and_view_results():
    """Run tests and open the HTML report in a browser"""
    # Run the tests
    print("Running tests...")
    subprocess.run(["pytest", "--html=test-report.html", "--self-contained-html"], check=False)
    
    # Check if the report was generated
    report_path = Path("test-report.html")
    if not report_path.exists():
        print(f"Error: Test report not found at {report_path}")
        return 1
    
    # Open the report in a browser
    print(f"Opening test report: {report_path}")
    webbrowser.open(str(report_path.absolute()))
    
    return 0

if __name__ == "__main__":
    sys.exit(run_tests_and_view_results())
