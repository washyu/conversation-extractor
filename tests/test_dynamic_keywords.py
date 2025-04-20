"""
Tests for the dynamic keyword generation functionality
"""
import os
import tempfile
import pytest
from conversation_extractor import (
    generate_dynamic_keywords,
    KeywordTracker,
    extract_topics,
    load_conversation
)


def test_generate_dynamic_keywords_basic():
    """
    FEATURE: Basic dynamic keyword generation

    Test that we can extract keywords from a conversation dynamically.
    """
    # Given a simple conversation
    conversation = """
    USER: I'm having trouble with my Python code. It keeps giving me errors with dictionaries.
    ASSISTANT: Let's look at your dictionary code. Are you using the correct syntax for accessing keys?
    USER: I think so. I'm using mydict['key'] but it says KeyError.
    ASSISTANT: That means the key doesn't exist in the dictionary. You should check if the key exists first.
    USER: How do I do that?
    ASSISTANT: You can use the 'in' operator like this: if 'key' in mydict:
    USER: That's helpful! Also, I'm working on a Flask project and need to handle form data.
    ASSISTANT: Flask's request object has a form attribute that contains form data as a dictionary.
    """

    # When we generate dynamic keywords
    keywords = generate_dynamic_keywords(conversation)

    # Then we should get relevant keywords
    assert len(keywords) > 0, "Should generate at least one keyword"
    assert any("dictionary" in kw.lower() for kw in keywords), "Should identify 'dictionary' as a keyword"
    # Note: 'key' might be filtered out as it's a short word, so we'll check for related terms
    assert any(kw.lower() in ["key", "keys", "keyerror", "keyword"] for kw in keywords) or \
           any("dict" in kw.lower() for kw in keywords), "Should identify dictionary-related keywords"

    # And the keywords should be sorted by length (longer first)
    for i in range(len(keywords) - 1):
        assert len(keywords[i]) >= len(keywords[i+1]), "Keywords should be sorted by length"


def test_generate_dynamic_keywords_with_existing():
    """
    FEATURE: Dynamic keyword generation with existing keywords

    Test that dynamic keyword generation respects existing keywords.
    """
    # Given a simple conversation
    conversation = """
    USER: I'm having trouble with my Python code. It keeps giving me errors with dictionaries.
    ASSISTANT: Let's look at your dictionary code. Are you using the correct syntax for accessing keys?
    USER: I think so. I'm using mydict['key'] but it says KeyError.
    ASSISTANT: That means the key doesn't exist in the dictionary. You should check if the key exists first.
    """

    # And some existing keywords
    existing_keywords = ["dictionary", "Python"]

    # When we generate dynamic keywords
    keywords = generate_dynamic_keywords(conversation, existing_keywords=existing_keywords)

    # Then we should not get duplicates of existing keywords
    assert "dictionary" not in keywords, "Should not duplicate existing keywords"
    assert "Python" not in keywords, "Should not duplicate existing keywords"

    # But we should still get other relevant keywords
    assert len(keywords) > 0, "Should generate at least one keyword"


def test_keyword_tracker():
    """
    FEATURE: Keyword importance tracking

    Test that the KeywordTracker can track keyword importance over time.
    """
    # Given a temporary file for persistence
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        temp_path = temp.name

    try:
        # And a keyword tracker
        tracker = KeywordTracker(persistence_file=temp_path)

        # When we update keywords
        tracker.update_keyword("Python", 1.0)
        tracker.update_keyword("Flask", 0.8)
        tracker.update_keyword("Python", 0.5)  # Update Python again

        # Then the importance should be tracked correctly
        top_keywords = tracker.get_top_keywords()
        assert len(top_keywords) == 2, "Should have two keywords"
        assert top_keywords[0][0] == "Python", "Python should be the most important keyword"
        assert top_keywords[0][1] > top_keywords[1][1], "Python should have higher importance than Flask"

        # And when we create a new tracker with the same persistence file
        new_tracker = KeywordTracker(persistence_file=temp_path)

        # Then it should load the existing data
        assert len(new_tracker.keywords) == 2, "Should load two keywords"
        assert "Python" in new_tracker.keywords, "Should load Python keyword"
        assert "Flask" in new_tracker.keywords, "Should load Flask keyword"

    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_extract_topics_with_dynamic_keywords():
    """
    FEATURE: Topic extraction with dynamic keywords

    Test that extract_topics can use dynamic keyword generation.
    """
    # Given a conversation with mixed topics
    conversation = """
    USER: I'm having trouble with my Python code. It keeps giving me errors with dictionaries.
    ASSISTANT: Let's look at your dictionary code. Are you using the correct syntax for accessing keys?
    USER: I think so. I'm using mydict['key'] but it says KeyError.
    ASSISTANT: That means the key doesn't exist in the dictionary. You should check if the key exists first.
    USER: How do I do that?
    ASSISTANT: You can use the 'in' operator like this: if 'key' in mydict:
    USER: That's helpful! Also, I'm working on a Flask project and need to handle form data.
    ASSISTANT: Flask's request object has a form attribute that contains form data as a dictionary.
    USER: I'm also struggling with focus today. My ADHD is making it hard to concentrate.
    ASSISTANT: That's understandable. Have you tried using the Pomodoro technique? 25 minutes of focus followed by a 5-minute break?
    USER: No, I haven't. That sounds like it could help.
    ASSISTANT: It's very effective for many people with ADHD. The time-boxing helps maintain focus for short periods.
    """

    # When we extract topics with dynamic keywords enabled
    topic_results = extract_topics(conversation, enable_dynamic=True)

    # Then we should get the standard categories
    assert "Python Syntax" in topic_results, "Should find Python Syntax category"
    assert "Web Development" in topic_results, "Should find Web Development category"
    assert "ADHD & Productivity" in topic_results, "Should find ADHD & Productivity category"

    # And we should also get a Dynamic Topics category
    assert "Dynamic Topics" in topic_results, "Should find Dynamic Topics category"
    assert len(topic_results["Dynamic Topics"]) > 0, "Should have at least one dynamic topic match"


def test_extract_topics_without_dynamic_keywords():
    """
    FEATURE: Topic extraction without dynamic keywords

    Test that extract_topics works correctly with dynamic keywords disabled.
    """
    # Given a conversation with mixed topics
    conversation = """
    USER: I'm having trouble with my Python code. It keeps giving me errors with dictionaries.
    ASSISTANT: Let's look at your dictionary code. Are you using the correct syntax for accessing keys?
    USER: I think so. I'm using mydict['key'] but it says KeyError.
    ASSISTANT: That means the key doesn't exist in the dictionary. You should check if the key exists first.
    """

    # When we extract topics with dynamic keywords disabled
    topic_results = extract_topics(conversation, enable_dynamic=False)

    # Then we should get the standard categories
    assert "Python Syntax" in topic_results, "Should find Python Syntax category"

    # But we should not get a Dynamic Topics category
    assert "Dynamic Topics" not in topic_results, "Should not find Dynamic Topics category"


def test_dynamic_keywords_with_real_conversation():
    """
    FEATURE: Dynamic keyword generation with real conversation

    Test dynamic keyword generation with a real conversation file.
    """
    # Given a real conversation file
    sample_file = os.path.join(os.path.dirname(__file__), "data", "coding_buddy_conversation.txt")
    assert os.path.exists(sample_file), f"Sample file '{sample_file}' not found"

    # When we load the conversation
    conversation = load_conversation(sample_file)
    assert conversation, "Failed to load conversation"

    # And generate dynamic keywords
    keywords = generate_dynamic_keywords(conversation)

    # Then we should get meaningful keywords
    assert len(keywords) > 5, "Should generate at least 5 keywords from a real conversation"

    # And when we extract topics with dynamic keywords
    topic_results = extract_topics(conversation, enable_dynamic=True)

    # Then we should get a Dynamic Topics category
    assert "Dynamic Topics" in topic_results, "Should find Dynamic Topics category"
    assert len(topic_results["Dynamic Topics"]) > 0, "Should have at least one dynamic topic match"

    # Print the dynamic keywords for inspection
    print("\nDynamic keywords generated from real conversation:")
    print(", ".join(keywords))

    # Print the dynamic topic matches for inspection
    print("\nDynamic topic matches:")
    for keyword, matched_line, _ in topic_results["Dynamic Topics"][:5]:  # Show first 5
        print(f"- {keyword}: {matched_line[:50]}...")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
