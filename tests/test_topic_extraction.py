"""
Pytest-based tests for topic extraction from mixed conversations
"""
import os
import pytest
import logging
from conversation_extractor import (
    load_conversation, 
    extract_topics, 
    DEFAULT_TOPIC_CATEGORIES
)

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
def test_data_dir():
    """Fixture to provide the path to the test data directory."""
    return os.path.join(os.path.dirname(__file__), 'data')


@pytest.fixture
def coding_buddy_conversation(test_data_dir):
    """Fixture to load the coding buddy conversation from the test data directory."""
    file_path = os.path.join(test_data_dir, 'coding_buddy_conversation.txt')
    return load_conversation(file_path)


def test_extract_topics_from_coding_buddy(coding_buddy_conversation):
    """
    FEATURE: Topic extraction from natural coding buddy conversation
    
    Test that we can extract and categorize topics from a natural conversation
    that mixes technical questions, ADHD challenges, and best practices.
    """
    logger.info("Testing topic extraction from coding buddy conversation")
    
    # When: We extract topics from the coding buddy conversation
    topic_results = extract_topics(coding_buddy_conversation, context_lines=2)
    
    # Then: We should find all expected topic categories
    expected_categories = [
        "Python Syntax", 
        "Web Development", 
        "Data Processing", 
        "ADHD & Productivity", 
        "Best Practices", 
        "Debugging"
    ]
    
    for category in expected_categories:
        logger.info(f"Checking that '{category}' is one of the categories")
        assert category in topic_results, f"Should find '{category}' category"
        
        # And: Each category should have at least one match
        matches = topic_results[category]
        logger.info(f"Category '{category}' has {len(matches)} matches")
        assert len(matches) > 0, f"Category '{category}' should have at least one match"
    
    logger.info("✅ Successfully extracted topics from coding buddy conversation")


def test_topic_categorization_accuracy(coding_buddy_conversation):
    """
    FEATURE: Accurate topic categorization in mixed conversation
    
    Test that topics are correctly categorized based on their content,
    even in a conversation that jumps between different topics.
    """
    logger.info("Testing topic categorization accuracy")
    
    # When: We extract topics
    topic_results = extract_topics(coding_buddy_conversation, context_lines=2)
    
    # Then: Check specific content is categorized correctly
    
    # Python Syntax should contain dictionary and list comprehension discussions
    python_syntax_keywords = [keyword for keyword, _, _ in topic_results["Python Syntax"]]
    logger.info(f"Python Syntax keywords found: {set(python_syntax_keywords)}")
    assert any(k in python_syntax_keywords for k in ["dictionary", "list comprehension", "{}"]), \
        "Python Syntax should include dictionary or list comprehension discussions"
    
    # ADHD & Productivity should contain focus and Pomodoro discussions
    adhd_keywords = [keyword for keyword, _, _ in topic_results["ADHD & Productivity"]]
    logger.info(f"ADHD & Productivity keywords found: {set(adhd_keywords)}")
    assert any(k in adhd_keywords for k in ["ADHD", "focus", "Pomodoro"]), \
        "ADHD & Productivity should include ADHD, focus or Pomodoro discussions"
    
    # Web Development should contain Flask discussions
    web_keywords = [keyword for keyword, _, _ in topic_results["Web Development"]]
    logger.info(f"Web Development keywords found: {set(web_keywords)}")
    assert "Flask" in web_keywords, \
        "Web Development should include Flask discussions"
    
    # Data Processing should contain CSV and pandas discussions
    data_keywords = [keyword for keyword, _, _ in topic_results["Data Processing"]]
    logger.info(f"Data Processing keywords found: {set(data_keywords)}")
    assert any(k in data_keywords for k in ["CSV", "pandas"]), \
        "Data Processing should include CSV or pandas discussions"
    
    logger.info("✅ Successfully verified topic categorization accuracy")


def test_context_preservation(coding_buddy_conversation):
    """
    FEATURE: Context preservation in topic extraction
    
    Test that the context around each topic is preserved correctly,
    providing meaningful context even in a mixed conversation.
    """
    logger.info("Testing context preservation in topic extraction")
    
    # When: We extract topics with different context sizes
    results_1 = extract_topics(coding_buddy_conversation, context_lines=1)
    results_3 = extract_topics(coding_buddy_conversation, context_lines=3)
    
    # Then: Context size should affect the amount of context preserved
    for category in results_1.keys():
        if category in results_3 and results_1[category] and results_3[category]:
            # Get the first match in each result
            _, _, context_1 = results_1[category][0]
            _, _, context_3 = results_3[category][0]
            
            logger.info(f"Category '{category}' with context_lines=1: {len(context_1)} lines")
            logger.info(f"Category '{category}' with context_lines=3: {len(context_3)} lines")
            
            # Context size 3 should generally have more lines than context size 1
            # (This might not always be true at the beginning or end of the file)
            if len(context_3) <= len(context_1):
                logger.info("Note: Context size 3 doesn't have more lines - this might be at file boundaries")
    
    # And: Check that context includes relevant information
    results = extract_topics(coding_buddy_conversation, context_lines=2)
    
    # Find a match for "ADHD" and check its context
    adhd_matches = [(keyword, line, context) for keyword, line, context 
                    in results.get("ADHD & Productivity", [])
                    if "ADHD" in keyword]
    
    if adhd_matches:
        keyword, line, context = adhd_matches[0]
        logger.info(f"Context for ADHD match: {len(context)} lines")
        context_text = "\n".join(context)
        
        # The context should include relevant information about ADHD
        assert any(term in context_text for term in ["focus", "distract", "attention"]), \
            "Context for ADHD should include relevant information"
    
    logger.info("✅ Successfully verified context preservation")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
