"""
Command-line interface for the conversation context extractor.
"""
import os
import argparse
from .extractor import load_conversation, extract_context, print_results


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Extract context around keywords in conversation text files."
    )
    parser.add_argument(
        "file", 
        help="Path to the conversation text file"
    )
    parser.add_argument(
        "-k", "--keywords", 
        required=True,
        help="Comma-separated list of keywords to search for"
    )
    parser.add_argument(
        "-c", "--context", 
        type=int, 
        default=3,
        help="Number of context lines to include before and after matches (default: 3)"
    )
    
    args = parser.parse_args()
    
    # Check if file exists
    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found.")
        return 1
    
    # Parse keywords
    keywords = [k.strip() for k in args.keywords.split(',') if k.strip()]
    if not keywords:
        print("Error: No valid keywords provided.")
        return 1
    
    # Load the conversation
    conversation = load_conversation(args.file)
    if not conversation:
        return 1
    
    print(f"Loaded conversation ({len(conversation)} characters, {len(conversation.split('\\n'))} lines)")
    print(f"Searching for keywords: {', '.join(keywords)}")
    print(f"Context lines: {args.context}")
    
    # Extract and print context
    results = extract_context(conversation, keywords, args.context)
    print_results(results)
    
    return 0


if __name__ == "__main__":
    exit(main())
