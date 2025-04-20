#!/usr/bin/env python
"""
Generate a CSP-compatible test report without inline scripts or styles.
This script runs pytest and captures the output to create a simple HTML report
that works with Jenkins' Content Security Policy restrictions.
"""
import os
import sys
import subprocess
import datetime
import re
from pathlib import Path

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

def run_tests_and_generate_report():
    """Run tests and generate a CSP-compatible HTML report"""
    # Create output directory if it doesn't exist
    output_dir = Path("test_reports")
    output_dir.mkdir(exist_ok=True)
    
    # Generate timestamp for the report filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = output_dir / f"csp_report_{timestamp}.html"
    
    # Run pytest with verbose output
    print(f"Running tests and generating CSP-compatible report to {report_file}...")
    result = subprocess.run(
        ["pytest", "-v"],
        capture_output=True,
        text=True
    )
    
    # Parse the output
    test_output = result.stdout
    
    # Generate HTML report
    html = generate_csp_compatible_html(test_output, result.returncode == 0)
    
    # Write the report to file
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"CSP-compatible report generated: {report_file}")
    
    # Also create a latest.html file that always points to the most recent report
    latest_file = output_dir / "csp_latest.html"
    with open(latest_file, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Latest CSP-compatible report: {latest_file}")
    
    # Return the exit code from pytest
    return result.returncode

def generate_csp_compatible_html(test_output, success):
    """Generate a CSP-compatible HTML report from the test output"""
    # Count the number of passed, failed, and skipped tests
    passed_count = test_output.count(" PASSED")
    failed_count = test_output.count(" FAILED")
    skipped_count = test_output.count(" SKIPPED")
    total_count = passed_count + failed_count + skipped_count
    
    # Format the test output as HTML
    test_output_html = test_output.replace("\n", "<br>")
    test_output_html = test_output_html.replace(" PASSED", '<span style="color: green;"> PASSED</span>')
    test_output_html = test_output_html.replace(" FAILED", '<span style="color: red;"> FAILED</span>')
    test_output_html = test_output_html.replace(" SKIPPED", '<span style="color: orange;"> SKIPPED</span>')
    
    # Generate the HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            color: #333;
        }}
        h1, h2 {{
            color: #2c3e50;
        }}
        .summary {{
            margin: 20px 0;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }}
        .summary-item {{
            display: inline-block;
            margin-right: 20px;
            padding: 5px 10px;
            border-radius: 3px;
        }}
        .total {{
            background-color: #e9ecef;
        }}
        .passed {{
            background-color: #d4edda;
            color: #155724;
        }}
        .failed {{
            background-color: #f8d7da;
            color: #721c24;
        }}
        .skipped {{
            background-color: #fff3cd;
            color: #856404;
        }}
        .output {{
            margin-top: 20px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
            overflow-x: auto;
            white-space: nowrap;
            font-family: monospace;
        }}
        .timestamp {{
            color: #6c757d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <h1>Test Report</h1>
    <p class="timestamp">Generated on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    
    <div class="summary">
        <h2>Summary</h2>
        <div class="summary-item total">Total: {total_count}</div>
        <div class="summary-item passed">Passed: {passed_count}</div>
        <div class="summary-item failed">Failed: {failed_count}</div>
        <div class="summary-item skipped">Skipped: {skipped_count}</div>
    </div>
    
    <h2>Test Output</h2>
    <div class="output">
        {test_output_html}
    </div>
</body>
</html>
"""
    
    return html

if __name__ == "__main__":
    sys.exit(run_tests_and_generate_report())
