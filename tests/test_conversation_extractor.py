"""
Pytest-based tests for the conversation context extractor
"""
import os
import pytest
from conversation_extractor import load_conversation, extract_context


@pytest.fixture
def sample_conversation():
    """Fixture to provide a sample conversation text for testing."""
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


@pytest.fixture
def sample_file(tmp_path, sample_conversation):
    """Fixture to create a temporary sample file."""
    file_path = tmp_path / "test_conversation.txt"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(sample_conversation)
    return file_path


def test_load_conversation(sample_file):
    """Test loading a conversation from a file."""
    content = load_conversation(sample_file)
    assert content is not None
    assert len(content) > 0
    assert "Python" in content
    assert "pandas" in content


def test_load_conversation_nonexistent_file():
    """Test loading from a nonexistent file."""
    content = load_conversation("nonexistent_file.txt")
    assert content == ""


def test_extract_context_single_keyword(sample_conversation):
    """Test extracting context for a single keyword."""
    results = extract_context(sample_conversation, ["Python"], context_lines=1)
    
    # Check that we found the keyword
    assert "Python" in results
    
    # Check that we found at least 2 occurrences
    assert len(results["Python"]) >= 2
    
    # Check that context is included
    first_match = results["Python"][0]
    matched_line, context = first_match
    
    # The matched line should contain "Python"
    assert "Python" in matched_line
    
    # Context should have at least 2 lines (matched line + 1 context line)
    assert len(context) >= 2


def test_extract_context_multiple_keywords(sample_conversation):
    """Test extracting context for multiple keywords."""
    results = extract_context(sample_conversation, ["Python", "pandas"], context_lines=1)
    
    # Check that both keywords were found
    assert "Python" in results
    assert "pandas" in results
    
    # Check pandas context
    pandas_match = results["pandas"][0]
    matched_line, context = pandas_match
    
    assert "pandas" in matched_line
    assert "numpy" in matched_line  # Should be in the same line
    assert len(context) >= 2  # At least 2 lines of context


def test_extract_context_no_matches(sample_conversation):
    """Test extracting context with no matches."""
    results = extract_context(sample_conversation, ["JavaScript"], context_lines=1)
    assert len(results) == 0


def test_extract_context_case_insensitive(sample_conversation):
    """Test that keyword matching is case insensitive."""
    results = extract_context(sample_conversation, ["python"], context_lines=1)
    assert "python" in results
    assert len(results["python"]) >= 2


def test_extract_context_boundaries(sample_conversation):
    """Test context extraction at the boundaries of the text."""
    # First line
    results = extract_context(sample_conversation, ["Hello"], context_lines=2)
    assert "Hello" in results
    first_match = results["Hello"][0]
    _, context = first_match
    # Should not go beyond the start of the text
    assert len(context) <= 3  # matched line + up to 2 context lines
    
    # Last line
    results = extract_context(sample_conversation, ["more questions"], context_lines=2)
    assert "more questions" in results
    last_match = results["more questions"][0]
    _, context = last_match
    # Should not go beyond the end of the text
    assert len(context) <= 3  # matched line + up to 2 context lines


def test_extract_context_varying_context_size(sample_conversation):
    """Test different context sizes."""
    # No context
    results_0 = extract_context(sample_conversation, ["Python"], context_lines=0)
    assert "Python" in results_0
    _, context_0 = results_0["Python"][0]
    assert len(context_0) == 1  # Just the matched line
    
    # Small context
    results_1 = extract_context(sample_conversation, ["Python"], context_lines=1)
    _, context_1 = results_1["Python"][0]
    assert len(context_1) > len(context_0)
    
    # Larger context
    results_3 = extract_context(sample_conversation, ["Python"], context_lines=3)
    _, context_3 = results_3["Python"][0]
    assert len(context_3) > len(context_1)


def test_real_file_integration(sample_file):
    """Integration test using a real file."""
    # Test the full workflow
    content = load_conversation(sample_file)
    results = extract_context(content, ["Python", "data"], context_lines=2)
    
    assert "Python" in results
    assert "data" in results
    assert len(results["Python"]) >= 2
    assert len(results["data"]) >= 1


if __name__ == "__main__":
    pytest.main(["-v", __file__])
