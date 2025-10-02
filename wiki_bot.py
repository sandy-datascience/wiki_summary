import wikipediaapi
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import re

# FORCE DOWNLOAD NLTK DATA
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

def simple_preprocess(text):
    """Clean text and ensure proper sentence capitalization"""
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # Split into sentences and capitalize each one
    sentences = nltk.sent_tokenize(text)
    sentences = [s.strip()[0].upper() + s.strip()[1:] if s.strip() else s for s in sentences]
    
    return ' '.join(sentences)

def wikisummary(query, n_sentence=5):
    wiki = wikipediaapi.Wikipedia('english')
    page = wiki.page(query)
    
    if not page.exists():
        return "Sorry, I couldn't find information on that topic."
    
    text = page.text
    
    if not text.strip():
        return "No content available for this topic."
    
    # Clean and capitalize text
    clean_text = simple_preprocess(text)
    sentences = nltk.sent_tokenize(clean_text)
    
    if len(sentences) == 0:
        return "No sentences found in the content."
    
    # Use TF-IDF for summarization
    tfidf = TfidfVectorizer(max_features=1000)
    
    try:
        tfidf_matrix = tfidf.fit_transform(sentences)
        doc_vector = tfidf.transform([" ".join(sentences)])
        scores = cosine_similarity(doc_vector, tfidf_matrix).flatten()
        
        n_select = min(n_sentence, len(sentences))
        top_indices = scores.argsort()[-n_select:][::-1]
        summary_sentences = [sentences[i] for i in sorted(top_indices)]
        
        return " ".join(summary_sentences)
        
    except Exception as e:
        return f"Error: {str(e)}"