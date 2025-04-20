"""
Conversation Context Extractor

This module reads a text file containing a conversation and extracts
context around specified keywords.
"""
import re
import os
from typing import List, Dict, Tuple


def load_conversation(file_path: str) -> str:
    """
    Load the conversation from a text file.
    
    Args:
        file_path: Path to the text file
        
    Returns:
        The content of the file as a string, or empty string if file not found
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error loading file: {e}")
        return ""


def extract_context(text: str, keywords: List[str], context_lines: int = 3) -> Dict[str, List[Tuple[str, List[str]]]]:
    """
    Extract context around keywords from text.
    
    Args:
        text: The full text to search in
        keywords: List of keywords to search for
        context_lines: Number of lines of context to include before and after the match
        
    Returns:
        Dictionary mapping keywords to lists of (matched line, context lines) tuples
    """
    results = {}
    
    # Split the text into lines
    lines = text.split('\n')
    
    # Process each keyword
    for keyword in keywords:
        keyword_results = []
        pattern = re.compile(rf'\b{re.escape(keyword)}\b', re.IGNORECASE)
        
        # Search for the keyword in each line
        for i, line in enumerate(lines):
            if pattern.search(line):
                # Get context lines before and after
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                
                context = lines[start:end]
                keyword_results.append((line, context))
        
        if keyword_results:
            results[keyword] = keyword_results
    
    return results


def print_results(results: Dict[str, List[Tuple[str, List[str]]]]) -> None:
    """
    Print the search results in a readable format.
    
    Args:
        results: Dictionary of search results from extract_context()
    """
    if not results:
        print("No matches found.")
        return
    
    for keyword, matches in results.items():
        print(f"\n{'='*80}")
        print(f"KEYWORD: '{keyword}' - {len(matches)} matches found")
        print(f"{'='*80}")
        
        for i, (matched_line, context) in enumerate(matches, 1):
            print(f"\nMatch #{i}:")
            print(f"{'-'*40}")
            for j, ctx_line in enumerate(context):
                # Highlight the line containing the keyword
                if ctx_line == matched_line:
                    print(f">>> {ctx_line}")
                else:
                    print(f"    {ctx_line}")
            print()
