# Conversation Context Extractor

A Python tool for extracting context around keywords in conversation text files.

## Features

- **Keyword Context Extraction**
  - Search for keywords in text conversations
  - Extract context around matches (configurable number of lines)
  - Case-insensitive matching

- **Topic Categorization**
  - Automatically categorize conversation topics
  - Predefined categories for Python, Web Development, ADHD, etc.
  - Support for custom topic categories
  - **Dynamic keyword generation** that adapts to conversation content
  - Keyword importance tracking over time

- **Multiple Interfaces**
  - Command-line interface
  - Python API for integration into other projects
  - Example scripts for quick usage

## Installation

```bash
# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux

# Install from the current directory
pip install -e .
```

## Usage

### Command Line

```bash
# Basic usage
conversation-extractor path/to/conversation.txt --keywords "keyword1,keyword2" --context 3

# Short form
conversation-extractor path/to/conversation.txt -k "keyword1,keyword2" -c 3
```

### Example Scripts

```bash
# Run the basic extractor example
python examples/run_extractor.py

# Run the topic extractor example
python examples/run_topic_extractor.py

# Run the dynamic keyword generation example
python examples/run_dynamic_keywords.py
```

### Python API

```python
# Basic context extraction
from conversation_extractor import load_conversation, extract_context, print_results

# Load a conversation from a file
text = load_conversation("path/to/conversation.txt")

# Search for keywords with 3 lines of context
results = extract_context(text, ["keyword1", "keyword2"], context_lines=3)

# Print the results
print_results(results)
```

### Topic Extraction API

```python
from conversation_extractor import load_conversation, extract_topics, print_topic_results

# Load a conversation from a file
text = load_conversation("path/to/conversation.txt")

# Extract topics with 2 lines of context
topic_results = extract_topics(text, context_lines=2)

# Print the topic results
print_topic_results(topic_results)

# Use custom topic categories
custom_categories = {
    "Python Data Structures": ["list", "dictionary", "tuple"],
    "Error Handling": ["try", "except", "error", "exception"]
}
topic_results = extract_topics(text, topic_categories=custom_categories, context_lines=2)
```

### Dynamic Keyword Generation API

```python
from conversation_extractor import load_conversation, generate_dynamic_keywords, KeywordTracker

# Load a conversation from a file
text = load_conversation("path/to/conversation.txt")

# Generate dynamic keywords
dynamic_keywords = generate_dynamic_keywords(text)
print(f"Generated {len(dynamic_keywords)} keywords: {dynamic_keywords[:5]}...")

# Extract topics with dynamic keywords enabled
from conversation_extractor import extract_topics
topic_results = extract_topics(text, enable_dynamic=True)

# Track keyword importance over time
tracker = KeywordTracker(persistence_file="keywords.json")

# Update keyword importance
for keyword in dynamic_keywords[:10]:  # Use top 10 keywords
    tracker.update_keyword(keyword)

# Get top keywords by importance
top_keywords = tracker.get_top_keywords(5)  # Get top 5 keywords
for keyword, importance in top_keywords:
    print(f"{keyword}: {importance:.2f}")
```

## Project Structure

```
conversation_extractor/  # Main package
├── __init__.py         # Package initialization
├── extractor.py        # Core functionality
├── topic_extractor.py  # Topic extraction functionality
├── dynamic_keywords.py # Dynamic keyword generation
└── cli.py              # Command-line interface
tests/                  # Test directory
├── __init__.py         # Makes tests a package
├── test_conversation_extractor.py  # Basic tests
├── test_topic_extractor.py        # Topic extraction tests
├── test_topic_extraction.py       # Integration tests
├── test_coding_buddy.py           # Natural conversation tests
├── test_dynamic_keywords.py        # Dynamic keyword tests
├── data/               # Test data
│   └── coding_buddy_conversation.txt
└── reports/            # Test reports
    ├── generate_report.py
    ├── run_tests.py
    └── run_detailed_tests.py
examples/               # Example scripts
├── run_extractor.py    # Basic extractor example
├── run_topic_extractor.py  # Topic extractor example
├── README.md           # Examples documentation
└── sample_conversation.txt  # Sample data for examples
setup.py                # Package installation
README.md               # Project documentation
```

## Development

### Running Tests

```bash
# Install pytest
pip install pytest

# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_conversation_extractor.py

# Run with detailed output
python tests/reports/run_tests.py

# Generate test report
python tests/reports/generate_report.py
```

## License

MIT
