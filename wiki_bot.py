import wikipediaapi
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

def simple_preprocess(text):
    """Simple preprocessing without complex tokenization"""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)  # remove URLs
    text = re.sub(r'\n+', ' ', text)  # remove multiple newlines
    text = re.sub(r'\s+', ' ', text)  # remove extra spaces
    return text.strip()

def wikisummary(query, n_sentence=5):
    """Simplified Wikipedia summary function"""
    wiki = wikipediaapi.Wikipedia('english')
    page = wiki.page(query)
    
    if not page.exists():
        return "Sorry, I couldn't find information on that topic."
    
    # Get page text directly (no recursive section processing)
    text = page.text
    
    if not text.strip():
        return "No content available for this topic."
    
    # Simple preprocessing
    clean_text = simple_preprocess(text)
    
    # Split into sentences
    sentences = nltk.sent_tokenize(clean_text)
    
    if len(sentences) == 0:
        return "No sentences found in the content."
    
    # Use TF-IDF for summarization
    tfidf = TfidfVectorizer(stop_words='english', max_features=1000)
    
    try:
        tfidf_matrix = tfidf.fit_transform(sentences)
        doc_vector = tfidf.transform([" ".join(sentences)])
        scores = cosine_similarity(doc_vector, tfidf_matrix).flatten()
        
        # Pick top sentences
        n_select = min(n_sentence, len(sentences))
        top_indices = scores.argsort()[-n_select:][::-1]
        
        # Get summary in original order
        summary_sentences = [sentences[i] for i in sorted(top_indices)]
        
        return " ".join(summary_sentences)
        
    except Exception as e:
        return f"Error: {str(e)}"

# Test
if __name__ == "__main__":
    result = wikisummary("Elon Musk", 3)
    print("Summary:")
    print(result)