#!/usr/bin/env python
"""
Generate a detailed test report with console output.
This script runs pytest and captures the output to create a more detailed HTML report.
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
    """Run tests and generate a detailed HTML report"""
    # Create output directory if it doesn't exist
    output_dir = Path("test_reports")
    output_dir.mkdir(exist_ok=True)
    
    # Generate timestamp for the report filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = output_dir / f"test_report_{timestamp}.html"
    
    # Run pytest with verbose output
    print(f"Running tests and generating report to {report_file}...")
    result = subprocess.run(
        ["pytest", "-v", "--no-header", "--no-summary"],
        capture_output=True,
        text=True
    )
    
    # Parse the output
    test_output = result.stdout
    
    # Generate HTML report
    html = generate_html_report(test_output, result.returncode == 0)
    
    # Write the report to file
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Report generated: {report_file}")
    
    # Also create a latest.html file that always points to the most recent report
    latest_file = output_dir / "latest.html"
    with open(latest_file, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Latest report: {latest_file}")
    
    # Return the exit code from pytest
    return result.returncode

def generate_html_report(test_output, success):
    """Generate an HTML report from the test output"""
    # Parse the test output to extract test results
    test_results = parse_test_output(test_output)
    
    # Count the number of passed, failed, and skipped tests
    passed = sum(1 for result in test_results if result["status"] == "PASSED")
    failed = sum(1 for result in test_results if result["status"] == "FAILED")
    skipped = sum(1 for result in test_results if result["status"] == "SKIPPED")
    total = len(test_results)
    
    # Generate the HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.5;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3 {{
            color: #2c3e50;
        }}
        .summary {{
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
        }}
        .summary-item {{
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
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
        .total {{
            background-color: #e9ecef;
            color: #495057;
        }}
        .test {{
            margin-bottom: 20px;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            overflow: hidden;
        }}
        .test-header {{
            padding: 10px 15px;
            font-weight: bold;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
        }}
        .test-header.passed {{
            background-color: #d4edda;
            color: #155724;
        }}
        .test-header.failed {{
            background-color: #f8d7da;
            color: #721c24;
        }}
        .test-header.skipped {{
            background-color: #fff3cd;
            color: #856404;
        }}
        .test-content {{
            padding: 15px;
            display: none;
        }}
        .test-content pre {{
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 0;
        }}
        .show {{
            display: block;
        }}
        .timestamp {{
            font-size: 0.8em;
            color: #6c757d;
        }}
        .search {{
            margin-bottom: 20px;
        }}
        .search input {{
            padding: 8px 12px;
            width: 100%;
            border: 1px solid #ced4da;
            border-radius: 4px;
        }}
        .filter-buttons {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }}
        .filter-button {{
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
        }}
        .filter-button.active {{
            box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.5);
        }}
        .filter-button.all {{
            background-color: #e9ecef;
            color: #495057;
        }}
        .filter-button.passed {{
            background-color: #d4edda;
            color: #155724;
        }}
        .filter-button.failed {{
            background-color: #f8d7da;
            color: #721c24;
        }}
        .filter-button.skipped {{
            background-color: #fff3cd;
            color: #856404;
        }}
        .hidden {{
            display: none;
        }}
    </style>
</head>
<body>
    <h1>Test Report</h1>
    <p class="timestamp">Generated on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    
    <div class="summary">
        <div class="summary-item total">Total: {total}</div>
        <div class="summary-item passed">Passed: {passed}</div>
        <div class="summary-item failed">Failed: {failed}</div>
        <div class="summary-item skipped">Skipped: {skipped}</div>
    </div>
    
    <div class="search">
        <input type="text" id="searchInput" placeholder="Search for tests...">
    </div>
    
    <div class="filter-buttons">
        <button class="filter-button all active" data-filter="all">All ({total})</button>
        <button class="filter-button passed" data-filter="passed">Passed ({passed})</button>
        <button class="filter-button failed" data-filter="failed">Failed ({failed})</button>
        <button class="filter-button skipped" data-filter="skipped">Skipped ({skipped})</button>
    </div>
    
    <div id="tests">
"""
    
    # Add each test result
    for i, result in enumerate(test_results):
        status_class = result["status"].lower()
        html += f"""
        <div class="test {status_class}">
            <div class="test-header {status_class}" onclick="toggleTest({i})">
                <span>{result["name"]}</span>
                <span>{result["status"]}</span>
            </div>
            <div class="test-content" id="test-{i}">
                <pre>{result["output"]}</pre>
            </div>
        </div>
"""
    
    # Add the JavaScript for interactivity
    html += """
    </div>
    
    <script>
        function toggleTest(id) {
            const content = document.getElementById(`test-${id}`);
            content.classList.toggle('show');
        }
        
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const tests = document.querySelectorAll('.test');
            
            tests.forEach(test => {
                const testName = test.querySelector('.test-header span').textContent.toLowerCase();
                if (testName.includes(searchTerm)) {
                    test.classList.remove('hidden');
                } else {
                    test.classList.add('hidden');
                }
            });
        });
        
        // Filter functionality
        const filterButtons = document.querySelectorAll('.filter-button');
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Update active button
                filterButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                const filter = this.getAttribute('data-filter');
                const tests = document.querySelectorAll('.test');
                
                tests.forEach(test => {
                    if (filter === 'all' || test.classList.contains(filter)) {
                        test.classList.remove('hidden');
                    } else {
                        test.classList.add('hidden');
                    }
                });
            });
        });
        
        // Expand failed tests by default
        document.addEventListener('DOMContentLoaded', function() {
            const failedTests = document.querySelectorAll('.test.failed');
            failedTests.forEach((test, index) => {
                const testId = test.querySelector('.test-content').id.replace('test-', '');
                toggleTest(testId);
            });
        });
    </script>
</body>
</html>
"""
    
    return html

def parse_test_output(output):
    """Parse the pytest output to extract test results"""
    test_results = []
    current_test = None
    current_output = []
    
    # Regular expression to match test result lines
    test_pattern = re.compile(r'^(.+?)::(.+?) (.+?)$')
    
    for line in output.splitlines():
        # Check if this is a test result line
        match = test_pattern.match(line)
        if match:
            # If we were processing a test, save it
            if current_test:
                test_results.append({
                    "name": current_test["name"],
                    "status": current_test["status"],
                    "output": "\n".join(current_output)
                })
            
            # Start a new test
            file_path, test_name, status = match.groups()
            current_test = {
                "name": f"{file_path}::{test_name}",
                "status": status
            }
            current_output = [line]
        elif current_test:
            # Add this line to the current test's output
            current_output.append(line)
    
    # Add the last test if there is one
    if current_test:
        test_results.append({
            "name": current_test["name"],
            "status": current_test["status"],
            "output": "\n".join(current_output)
        })
    
    return test_results

if __name__ == "__main__":
    sys.exit(run_tests_and_generate_report())
