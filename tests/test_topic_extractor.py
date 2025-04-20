"""
Pytest-based tests for the topic extractor functionality
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
def mixed_conversation():
    """Fixture to provide a sample mixed conversation text for testing."""
    return """USER: I'm having trouble remembering Python dictionary syntax. What's the best way to create and update dictionaries?

A: Python dictionaries are super useful! Here's a refresher on dictionary syntax:

### Creating Dictionaries

1. **Empty dictionary**:
```python
my_dict = {}
```

2. **Dictionary with initial values**:
```python
person = {
    "name": "John",
    "age": 30,
    "city": "New York"
}
```

USER: Sorry, I got distracted. I have ADHD and sometimes struggle to focus on coding tasks. Do you have any tips for staying focused while coding?

A: I completely understand! Many developers with ADHD find coding both rewarding and challenging. Here are some strategies that might help:

1. **Use the Pomodoro Technique**: Work for 25 minutes, then take a 5-minute break. After 4 cycles, take a longer break (15-30 minutes).

2. **Body Doubling**: Code with someone else (in person or virtually). Having someone else working alongside you can help maintain focus.

USER: Thanks for the tips! Now, what's the best way to handle file uploads in Flask?

A: Handling file uploads in Flask is straightforward. Here's how to implement it:

In your app.py file:
```python
import os
from flask import Flask, request, render_template, redirect, url_for
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}
```"""


@pytest.fixture
def sample_file(tmp_path, mixed_conversation):
    """Fixture to create a temporary sample file."""
    file_path = tmp_path / "test_mixed_conversation.txt"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(mixed_conversation)
    return file_path


def test_extract_topics_basic(mixed_conversation):
    """
    FEATURE: Topic extraction from mixed conversation
    
    Test that we can extract and categorize topics from a mixed conversation.
    """
    logger.info("Testing basic topic extraction from mixed conversation")
    
    # When: We extract topics from a mixed conversation
    topic_results = extract_topics(mixed_conversation, context_lines=1)
    
    # Then: We should find multiple topic categories
    logger.info(f"Found {len(topic_results)} topic categories")
    assert len(topic_results) >= 3, "Should find at least 3 topic categories"
    
    # And: Python Syntax should be one of the categories
    logger.info("Checking that 'Python Syntax' is one of the categories")
    assert "Python Syntax" in topic_results, "Should find 'Python Syntax' category"
    
    # And: ADHD & Productivity should be one of the categories
    logger.info("Checking that 'ADHD & Productivity' is one of the categories")
    assert "ADHD & Productivity" in topic_results, "Should find 'ADHD & Productivity' category"
    
    # And: Web Development should be one of the categories
    logger.info("Checking that 'Web Development' is one of the categories")
    assert "Web Development" in topic_results, "Should find 'Web Development' category"
    
    logger.info("✅ Successfully extracted topics from mixed conversation")


def test_extract_topics_custom_categories(mixed_conversation):
    """
    FEATURE: Custom topic categories
    
    Test that we can use custom topic categories for extraction.
    """
    logger.info("Testing topic extraction with custom categories")
    
    # Given: Custom topic categories
    custom_categories = {
        "Python Data Structures": ["dictionary", "list", "tuple", "set", "{}"],
        "Mental Health": ["ADHD", "focus", "distraction", "attention"],
        "Web Frameworks": ["Flask", "Django", "FastAPI"]
    }
    
    # When: We extract topics using custom categories
    topic_results = extract_topics(
        mixed_conversation, 
        topic_categories=custom_categories,
        context_lines=1
    )
    
    # Then: We should find our custom categories
    logger.info(f"Found {len(topic_results)} custom topic categories")
    
    # And: Python Data Structures should be one of the categories
    logger.info("Checking that 'Python Data Structures' is one of the categories")
    assert "Python Data Structures" in topic_results, "Should find 'Python Data Structures' category"
    
    # And: Mental Health should be one of the categories
    logger.info("Checking that 'Mental Health' is one of the categories")
    assert "Mental Health" in topic_results, "Should find 'Mental Health' category"
    
    # And: Web Frameworks should be one of the categories
    logger.info("Checking that 'Web Frameworks' is one of the categories")
    assert "Web Frameworks" in topic_results, "Should find 'Web Frameworks' category"
    
    logger.info("✅ Successfully extracted topics with custom categories")


def test_extract_topics_context_size(mixed_conversation):
    """
    FEATURE: Context size in topic extraction
    
    Test that different context sizes work correctly in topic extraction.
    """
    logger.info("Testing different context sizes in topic extraction")
    
    # When: We extract topics with different context sizes
    results_1 = extract_topics(mixed_conversation, context_lines=1)
    results_3 = extract_topics(mixed_conversation, context_lines=3)
    
    # Then: Both should find the same categories
    logger.info(f"Context size 1: {len(results_1)} categories")
    logger.info(f"Context size 3: {len(results_3)} categories")
    assert set(results_1.keys()) == set(results_3.keys()), "Should find the same categories regardless of context size"
    
    # But: Context size 3 should have more context lines
    category = next(iter(results_1.keys()))  # Get the first category
    if category in results_1 and category in results_3 and results_1[category] and results_3[category]:
        _, _, context_1 = results_1[category][0]
        _, _, context_3 = results_3[category][0]
        logger.info(f"Context size 1: {len(context_1)} lines in first match")
        logger.info(f"Context size 3: {len(context_3)} lines in first match")
        assert len(context_3) > len(context_1), "Context size 3 should have more lines than context size 1"
    
    logger.info("✅ Successfully handled different context sizes in topic extraction")


def test_extract_topics_from_file(sample_file):
    """
    FEATURE: Topic extraction from file
    
    Test the full workflow from loading a file to extracting topics.
    """
    logger.info(f"Testing topic extraction from file: {sample_file}")
    
    # When: We load a file and extract topics
    conversation = load_conversation(sample_file)
    topic_results = extract_topics(conversation, context_lines=2)
    
    # Then: We should find multiple topic categories
    logger.info(f"Found {len(topic_results)} topic categories")
    assert len(topic_results) >= 3, "Should find at least 3 topic categories"
    
    # And: We should find matches in each category
    for category, matches in topic_results.items():
        logger.info(f"Category '{category}' has {len(matches)} matches")
        assert len(matches) > 0, f"Category '{category}' should have at least one match"
    
    logger.info("✅ Successfully extracted topics from file")


def test_topic_categorization(mixed_conversation):
    """
    FEATURE: Correct topic categorization
    
    Test that topics are correctly categorized based on their content.
    """
    logger.info("Testing correct topic categorization")
    
    # When: We extract topics
    topic_results = extract_topics(mixed_conversation, context_lines=2)
    
    # Then: Dictionary-related content should be in Python Syntax
    if "Python Syntax" in topic_results:
        python_syntax_keywords = [keyword for keyword, _, _ in topic_results["Python Syntax"]]
        logger.info(f"Python Syntax keywords found: {python_syntax_keywords}")
        assert "dictionary" in python_syntax_keywords or "{}" in python_syntax_keywords, \
            "Dictionary-related content should be categorized under Python Syntax"
    
    # And: ADHD-related content should be in ADHD & Productivity
    if "ADHD & Productivity" in topic_results:
        adhd_keywords = [keyword for keyword, _, _ in topic_results["ADHD & Productivity"]]
        logger.info(f"ADHD & Productivity keywords found: {adhd_keywords}")
        assert "ADHD" in adhd_keywords or "focus" in adhd_keywords, \
            "ADHD-related content should be categorized under ADHD & Productivity"
    
    # And: Flask-related content should be in Web Development
    if "Web Development" in topic_results:
        web_keywords = [keyword for keyword, _, _ in topic_results["Web Development"]]
        logger.info(f"Web Development keywords found: {web_keywords}")
        assert "Flask" in web_keywords, \
            "Flask-related content should be categorized under Web Development"
    
    logger.info("✅ Successfully verified correct topic categorization")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
