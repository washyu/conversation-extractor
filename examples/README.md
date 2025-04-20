# Conversation Extractor Examples

This directory contains example scripts demonstrating how to use the Conversation Extractor package.

## Available Examples

### Basic Context Extraction

`run_extractor.py` - Demonstrates how to extract context around keywords in a conversation.

```bash
python run_extractor.py
```

This script:
1. Loads a conversation from a text file
2. Prompts you to enter keywords to search for
3. Asks for the number of context lines to include
4. Extracts and displays the context around the keywords

### Topic Extraction

`run_topic_extractor.py` - Demonstrates how to extract and categorize topics in a conversation.

```bash
python run_topic_extractor.py
```

This script:
1. Loads a conversation from a text file
2. Extracts topics based on predefined categories
3. Displays the extracted topics with context
4. Shows a summary of the topics found

### Dynamic Keyword Generation

`run_dynamic_keywords.py` - Demonstrates how to dynamically generate keywords from a conversation.

```bash
python run_dynamic_keywords.py
```

This script:
1. Loads a conversation from a text file
2. Generates dynamic keywords based on the conversation content
3. Extracts topics using the dynamic keywords
4. Demonstrates keyword importance tracking

## Using Your Own Conversations

To use these examples with your own conversation files:

1. Create a text file named `sample_conversation.txt` in this directory
2. Run the example scripts as described above

Alternatively, the scripts will use the sample conversation from the test data directory if available.
