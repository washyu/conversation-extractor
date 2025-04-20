"""
Dynamic Keyword Generator Module

Analyze conversation to dynamically extract new potential keywords.
"""
import os
import re
import json
from collections import Counter


def generate_dynamic_keywords(conversation_text, existing_keywords=None, threshold=0.5):
    """
    Analyze conversation to dynamically extract new potential keywords.

    Args:
        conversation_text: The conversation text to analyze
        existing_keywords: Optional list of already known keywords to avoid duplicates
        threshold: Importance threshold for considering a term as a keyword

    Returns:
        List of new potential keywords
    """
    import nltk
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.corpus import stopwords
    from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder

    # Ensure NLTK resources are downloaded
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('punkt')
        nltk.download('stopwords')

    # Prepare existing keywords
    existing_keywords = existing_keywords or []
    existing_keywords_lower = [k.lower() for k in existing_keywords]

    # Ensure NLTK resources are downloaded
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('punkt')
        nltk.download('stopwords')

    # Tokenize the conversation
    try:
        sentences = sent_tokenize(conversation_text)
    except LookupError:
        # Fallback to simple sentence splitting if NLTK tokenizer fails
        sentences = [s.strip() for s in re.split(r'[.!?]+', conversation_text) if s.strip()]

    try:
        words = [word_tokenize(sentence) for sentence in sentences]
    except LookupError:
        # Fallback to simple word splitting if NLTK tokenizer fails
        words = [re.findall(r'\w+', sentence) for sentence in sentences]

    flat_words = [word.lower() for sentence in words for word in sentence
                 if word.isalnum() and len(word) > 2]

    # Remove stopwords
    try:
        stop_words = set(stopwords.words('english'))
    except (LookupError, AttributeError):
        # Fallback to a basic set of stopwords if NLTK stopwords fail
        stop_words = {'a', 'an', 'the', 'and', 'or', 'but', 'if', 'because', 'as', 'what',
                      'while', 'of', 'to', 'in', 'for', 'with', 'by', 'about', 'against',
                      'between', 'into', 'through', 'during', 'before', 'after', 'above',
                      'below', 'from', 'up', 'down', 'on', 'off', 'over', 'under', 'again',
                      'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
                      'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
                      'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
                      'can', 'will', 'just', 'should', 'now'}

    filtered_words = [word for word in flat_words if word not in stop_words]

    # Find frequent terms
    word_freq = Counter(filtered_words)
    total_words = len(filtered_words)

    # Find bigrams (two-word phrases)
    try:
        bigram_finder = BigramCollocationFinder.from_words(flat_words)
        bigram_finder.apply_freq_filter(2)  # Only consider bigrams that appear >= 2 times
        bigrams = bigram_finder.nbest(BigramAssocMeasures.pmi, 20)
    except Exception:
        # Fallback to simple bigram counting if NLTK collocations fail
        bigrams = []
        if len(flat_words) > 1:
            for i in range(len(flat_words) - 1):
                bigrams.append((flat_words[i], flat_words[i+1]))

    # Combine individual words and bigrams
    potential_keywords = []

    # Add important single words
    for word, count in word_freq.most_common(30):
        # Skip if already in existing keywords
        if word.lower() in existing_keywords_lower:
            continue

        # Calculate importance score based on frequency
        importance = count / total_words
        if importance > threshold / 4:  # Lower threshold for single words
            potential_keywords.append(word)

    # Add important bigrams
    for w1, w2 in bigrams:
        bigram = f"{w1} {w2}"
        # Skip if already in existing keywords
        if bigram.lower() in existing_keywords_lower:
            continue

        # Get combined frequency
        combined_count = sum(1 for i in range(len(flat_words)-1)
                           if flat_words[i] == w1 and flat_words[i+1] == w2)

        # Calculate importance score
        importance = combined_count / total_words
        if importance > threshold / 2:  # Moderate threshold for bigrams
            potential_keywords.append(bigram)

    # Analyze sentences for key phrases
    for i, sentence in enumerate(sentences):
        # Look for sentences with potential importance markers
        sentence_lower = sentence.lower()
        if any(marker in sentence_lower for marker in
              ["important", "remember", "key", "crucial", "essential",
               "don't forget", "note that", "keep in mind"]):
            # Extract the next sentence as it might contain key information
            if i + 1 < len(sentences):
                next_sentence = sentences[i + 1]
                # Extract potential keywords from this sentence
                try:
                    next_words = word_tokenize(next_sentence)
                except LookupError:
                    next_words = re.findall(r'\w+', next_sentence)

                for word in next_words:
                    if (word.isalnum() and len(word) > 3 and
                        word.lower() not in stop_words and
                        word.lower() not in existing_keywords_lower and
                        word.lower() not in [k.lower() for k in potential_keywords]):
                        potential_keywords.append(word)

    # Remove duplicates and sort by length (preferring longer keywords)
    unique_keywords = sorted(set(potential_keywords), key=len, reverse=True)

    return unique_keywords[:20]  # Return top 20 new keywords


class KeywordTracker:
    """Track keywords and their importance over time."""

    def __init__(self, persistence_file=None):
        """
        Initialize the keyword tracker.

        Args:
            persistence_file: Optional file path to save/load keyword data
        """
        self.keywords = {}  # Maps keywords to their importance scores
        self.persistence_file = persistence_file

        # Load existing data if available
        if persistence_file and os.path.exists(persistence_file):
            self._load()

    def update_keyword(self, keyword, importance_increment=1.0, decay_factor=0.9):
        """
        Update the importance of a keyword.

        Args:
            keyword: The keyword to update
            importance_increment: How much to increase importance
            decay_factor: Factor to decay existing keywords
        """
        # Decay all existing keywords
        for k in self.keywords:
            self.keywords[k] *= decay_factor

        # Update or add the new keyword
        if keyword in self.keywords:
            self.keywords[keyword] += importance_increment
        else:
            self.keywords[keyword] = importance_increment

        # Save if we have a persistence file
        if self.persistence_file:
            self._save()

    def get_top_keywords(self, n=20):
        """
        Get the top n keywords by importance.

        Args:
            n: Number of keywords to return

        Returns:
            List of (keyword, importance) tuples
        """
        return sorted(self.keywords.items(), key=lambda x: x[1], reverse=True)[:n]

    def _save(self):
        """Save keyword data to the persistence file."""
        with open(self.persistence_file, 'w') as f:
            json.dump(self.keywords, f)

    def _load(self):
        """Load keyword data from the persistence file."""
        try:
            with open(self.persistence_file, 'r') as f:
                self.keywords = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self.keywords = {}
