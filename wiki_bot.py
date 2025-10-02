import wikipediaapi
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# FORCE DOWNLOAD NLTK DATA
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')
    
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
    
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

def simple_preprocess(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def wikisummary(query, n_sentence=5):
    wiki = wikipediaapi.Wikipedia('english')
    page = wiki.page(query)
    
    if not page.exists():
        return "Sorry, I couldn't find information on that topic."
    
    text = page.text
    
    if not text.strip():
        return "No content available for this topic."
    
    clean_text = simple_preprocess(text)
    sentences = nltk.sent_tokenize(clean_text)
    
    if len(sentences) == 0:
        return "No sentences found in the content."
    
    tfidf = TfidfVectorizer(stop_words='english', max_features=1000)
    
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