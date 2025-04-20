"""
Download NLTK data required for dynamic keyword generation
"""
import nltk

def download_nltk_data():
    """Download required NLTK data."""
    print("Downloading NLTK data...")
    
    # Download punkt for sentence tokenization
    nltk.download('punkt')
    
    # Download stopwords for filtering common words
    nltk.download('stopwords')
    
    # Download wordnet for lemmatization
    nltk.download('wordnet')
    
    # Download averaged_perceptron_tagger for POS tagging
    nltk.download('averaged_perceptron_tagger')
    
    print("NLTK data download complete!")

if __name__ == "__main__":
    download_nltk_data()
