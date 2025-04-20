"""
Enhanced pytest-based tests for the conversation context extractor with detailed logging
"""
import os
import pytest
import logging
from conversation_extractor import load_conversation, extract_context

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Add a console handler with a custom formatter
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s: %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)


@pytest.fixture
def sample_conversation():
    """Fixture to provide a sample conversation text for testing."""
    logger.info("Creating sample conversation fixture")
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
    logger.info(f"Creating temporary sample file in {tmp_path}")
    file_path = tmp_path / "test_conversation.txt"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(sample_conversation)
    return file_path


def test_load_conversation(sample_file):
    """
    FEATURE: Loading conversation from file

    Test that we can successfully load a conversation from a file and
    the content is correctly read.
    """
    logger.info(f"Testing loading conversation from file: {sample_file}")

    # When: We load a conversation from a file
    content = load_conversation(sample_file)

    # Then: The content should be loaded correctly
    logger.info(f"Checking content is not None")
    assert content is not None, "Content should not be None"

    logger.info(f"Checking content is not empty (length: {len(content)})")
    assert len(content) > 0, "Content should not be empty"

    logger.info(f"Checking content contains expected keywords")
    assert "Python" in content, "Content should contain 'Python'"
    assert "pandas" in content, "Content should contain 'pandas'"

    logger.info("✅ Successfully loaded conversation from file")


def test_load_conversation_nonexistent_file():
    """
    FEATURE: Error handling for nonexistent files

    Test that attempting to load a nonexistent file returns an empty string
    instead of raising an exception.
    """
    nonexistent_file = "nonexistent_file.txt"
    logger.info(f"Testing loading from nonexistent file: {nonexistent_file}")

    # When: We try to load a nonexistent file
    content = load_conversation(nonexistent_file)

    # Then: We should get an empty string
    logger.info("Checking that an empty string is returned")
    assert content == "", "Should return empty string for nonexistent file"

    logger.info("✅ Successfully handled nonexistent file")


def test_extract_context_single_keyword(sample_conversation):
    """
    FEATURE: Extracting context for a single keyword

    Test that we can extract context around a single keyword with the
    correct number of context lines.
    """
    keyword = "Python"
    context_lines = 1
    logger.info(f"Testing context extraction for single keyword: '{keyword}' with {context_lines} context lines")

    # When: We extract context for a single keyword
    results = extract_context(sample_conversation, [keyword], context_lines=context_lines)

    # Then: We should find the keyword
    logger.info("Checking that the keyword was found")
    assert keyword in results, f"Keyword '{keyword}' should be found"

    # And: We should find at least 2 occurrences
    occurrences = len(results[keyword])
    logger.info(f"Found {occurrences} occurrences of '{keyword}'")
    assert occurrences >= 2, f"Should find at least 2 occurrences of '{keyword}'"

    # And: The matched line should contain the keyword
    first_match = results[keyword][0]
    matched_line, context = first_match
    logger.info(f"First matched line: '{matched_line}'")
    assert keyword in matched_line, f"Matched line should contain '{keyword}'"

    # And: Context should include the matched line plus context lines
    logger.info(f"Context has {len(context)} lines")
    assert len(context) >= 2, f"Context should have at least 2 lines (matched line + {context_lines} context line)"

    logger.info("✅ Successfully extracted context for single keyword")


def test_extract_context_multiple_keywords(sample_conversation):
    """
    FEATURE: Extracting context for multiple keywords

    Test that we can extract context around multiple keywords simultaneously.
    """
    keywords = ["Python", "pandas"]
    context_lines = 1
    logger.info(f"Testing context extraction for multiple keywords: {keywords} with {context_lines} context lines")

    # When: We extract context for multiple keywords
    results = extract_context(sample_conversation, keywords, context_lines=context_lines)

    # Then: We should find both keywords
    for keyword in keywords:
        logger.info(f"Checking that keyword '{keyword}' was found")
        assert keyword in results, f"Keyword '{keyword}' should be found"

    # And: The pandas match should contain both pandas and numpy
    pandas_match = results["pandas"][0]
    matched_line, context = pandas_match
    logger.info(f"Pandas matched line: '{matched_line}'")
    assert "pandas" in matched_line, "Matched line should contain 'pandas'"
    assert "numpy" in matched_line, "Matched line should contain 'numpy' (should be in the same line)"

    # And: Context should have the right number of lines
    logger.info(f"Context has {len(context)} lines")
    assert len(context) >= 2, f"Context should have at least 2 lines (matched line + {context_lines} context line)"

    logger.info("✅ Successfully extracted context for multiple keywords")


def test_extract_context_no_matches(sample_conversation):
    """
    FEATURE: Handling no matches

    Test that searching for keywords that don't exist returns an empty result.
    """
    keyword = "JavaScript"
    logger.info(f"Testing context extraction for non-existent keyword: '{keyword}'")

    # When: We search for a keyword that doesn't exist
    results = extract_context(sample_conversation, [keyword], context_lines=1)

    # Then: We should get an empty result
    logger.info(f"Checking that no results were found")
    assert len(results) == 0, "Should return empty results for non-existent keyword"

    logger.info("✅ Successfully handled no matches case")


def test_extract_context_case_insensitive(sample_conversation):
    """
    FEATURE: Case-insensitive matching

    Test that keyword matching is case-insensitive.
    """
    keyword = "python"  # lowercase, while text has "Python"
    logger.info(f"Testing case-insensitive matching for keyword: '{keyword}'")

    # When: We search for a keyword with different case
    results = extract_context(sample_conversation, [keyword], context_lines=1)

    # Then: We should still find it
    logger.info("Checking that the keyword was found despite case difference")
    assert keyword in results, f"Keyword '{keyword}' should be found (case-insensitive)"

    # And: We should find at least 2 occurrences
    occurrences = len(results[keyword])
    logger.info(f"Found {occurrences} occurrences of '{keyword}'")
    assert occurrences >= 2, f"Should find at least 2 occurrences of '{keyword}'"

    logger.info("✅ Successfully performed case-insensitive matching")


def test_extract_context_boundaries(sample_conversation):
    """
    FEATURE: Handling text boundaries

    Test that context extraction works correctly at the beginning and end of text.
    """
    # Test first line
    first_keyword = "Hello"
    context_lines = 2
    logger.info(f"Testing context extraction at the beginning of text with keyword: '{first_keyword}'")

    # When: We search for a keyword at the beginning
    results = extract_context(sample_conversation, [first_keyword], context_lines=context_lines)

    # Then: We should find it
    assert first_keyword in results, f"Keyword '{first_keyword}' should be found"

    # And: Context should not go beyond the start of the text
    first_match = results[first_keyword][0]
    _, context = first_match
    logger.info(f"Context at beginning has {len(context)} lines (should be <= {context_lines + 1})")
    assert len(context) <= 3, f"Context should have at most {context_lines + 1} lines at the beginning"

    # Test last line
    last_keyword = "more questions"
    logger.info(f"Testing context extraction at the end of text with keyword: '{last_keyword}'")

    # When: We search for a keyword at the end
    results = extract_context(sample_conversation, [last_keyword], context_lines=context_lines)

    # Then: We should find it
    assert last_keyword in results, f"Keyword '{last_keyword}' should be found"

    # And: Context should not go beyond the end of the text
    last_match = results[last_keyword][0]
    _, context = last_match
    logger.info(f"Context at end has {len(context)} lines (should be <= {context_lines + 1})")
    assert len(context) <= 3, f"Context should have at most {context_lines + 1} lines at the end"

    logger.info("✅ Successfully handled text boundaries")


def test_extract_context_varying_context_size(sample_conversation):
    """
    FEATURE: Different context sizes

    Test that different context sizes work correctly.
    """
    keyword = "Python"
    logger.info(f"Testing different context sizes for keyword: '{keyword}'")

    # Test with no context
    logger.info("Testing with context_lines=0 (no context)")
    results_0 = extract_context(sample_conversation, [keyword], context_lines=0)
    assert keyword in results_0, f"Keyword '{keyword}' should be found"
    _, context_0 = results_0[keyword][0]
    logger.info(f"Context size 0 has {len(context_0)} lines")
    assert len(context_0) == 1, "With context_lines=0, should only include the matched line"

    # Test with small context
    logger.info("Testing with context_lines=1 (small context)")
    results_1 = extract_context(sample_conversation, [keyword], context_lines=1)
    _, context_1 = results_1[keyword][0]
    logger.info(f"Context size 1 has {len(context_1)} lines")
    assert len(context_1) > len(context_0), "Context size 1 should have more lines than context size 0"

    # Test with larger context
    logger.info("Testing with context_lines=3 (larger context)")
    results_3 = extract_context(sample_conversation, [keyword], context_lines=3)
    _, context_3 = results_3[keyword][0]
    logger.info(f"Context size 3 has {len(context_3)} lines")
    assert len(context_3) > len(context_1), "Context size 3 should have more lines than context size 1"

    logger.info("✅ Successfully handled different context sizes")


def test_real_file_integration(sample_file):
    """
    FEATURE: End-to-end integration

    Test the full workflow from loading a file to extracting context.
    """
    keywords = ["Python", "data"]
    context_lines = 2
    logger.info(f"Testing full workflow: load file and extract context for keywords: {keywords}")

    # When: We load a file and extract context
    logger.info(f"Loading conversation from {sample_file}")
    content = load_conversation(sample_file)

    logger.info(f"Extracting context with {context_lines} context lines")
    results = extract_context(content, keywords, context_lines=context_lines)

    # Then: We should find both keywords
    for keyword in keywords:
        logger.info(f"Checking that keyword '{keyword}' was found")
        assert keyword in results, f"Keyword '{keyword}' should be found"

    # And: We should find the expected number of occurrences
    python_occurrences = len(results["Python"])
    data_occurrences = len(results["data"])
    logger.info(f"Found {python_occurrences} occurrences of 'Python'")
    logger.info(f"Found {data_occurrences} occurrences of 'data'")

    assert python_occurrences >= 2, "Should find at least 2 occurrences of 'Python'"
    assert data_occurrences >= 1, "Should find at least 1 occurrence of 'data'"

    logger.info("✅ Successfully completed end-to-end integration test")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
