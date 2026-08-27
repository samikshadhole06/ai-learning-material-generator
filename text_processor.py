import re
from collections import Counter


def clean_text(text):
    """
    Basic text cleaning.
    """
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_keywords(text, top_n=15):
    """
    Extract important keywords using simple frequency analysis.
    Works without spaCy for cloud deployment.
    """
    # Remove common words (simple stopwords)
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
                 'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
                 'could', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'}
    
    # Extract words
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Filter stopwords and count
    words = [word for word in words if word not in stopwords]
    word_freq = Counter(words)
    
    # Get top N words
    top_words = [word for word, freq in word_freq.most_common(top_n)]
    
    return top_words


def chunk_text(text, chunk_size=500, overlap=100):
    """
    Split text into overlapping chunks.
    """
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        
        if chunk.strip():
            chunks.append(chunk)
        
        start += (chunk_size - overlap)

    return chunks