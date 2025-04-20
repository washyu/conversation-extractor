"""
Pytest configuration file for enhanced test reporting
"""
import pytest
import os
import sys

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def pytest_configure(config):
    """Add custom markers"""
    config.addinivalue_line("markers", "conversation: tests for conversation extraction")
    config.addinivalue_line("markers", "topic: tests for topic extraction")
    config.addinivalue_line("markers", "dynamic: tests for dynamic keyword generation")


def pytest_runtest_setup(item):
    """Print a separator before each test"""
    print("\n" + "=" * 80)
    print(f"RUNNING TEST: {item.name}")
    print("-" * 80)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Add more detailed information to test reports"""
    outcome = yield
    report = outcome.get_result()
    
    # Add test docstring to report for better documentation in the HTML report
    if report.when == "call" and hasattr(item, "obj") and item.obj.__doc__:
        report.sections.append(("Test Description", item.obj.__doc__.strip()))
    
    # Add test parameters to report
    if report.when == "call" and hasattr(item, "funcargs"):
        params = {k: repr(v) for k, v in item.funcargs.items() if k != "request"}
        if params:
            report.sections.append(("Test Parameters", "\n".join(f"{k}: {v}" for k, v in params.items())))
