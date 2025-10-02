import wikipediaapi
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


def text_preprocessing(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)

    # Sentence tokenize
    sentences = nltk.sent_tokenize(text)

    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    cleaned_sentences = []

    for s in sentences:
        tokens = nltk.word_tokenize(s)
        tokens = [w for w in tokens if w not in stop_words]
        tokens = [lemmatizer.lemmatize(w) for w in tokens]
        cleaned_sentences.append(" ".join(tokens))

    return ". ".join(cleaned_sentences)


def para_processing(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)

    tokens = nltk.word_tokenize(text)

    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if w not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(w) for w in tokens]

    return " ".join(tokens)


def get_full_page_text(page):
    """Fixed function to get full page text"""
    skip_titles = ["References", "See also", "External links", "Further reading"]

    text = ""
    # Only include page text if title is not in skip list
    if page.title not in skip_titles and page.text.strip():
        text += page.text + "\n"

    # Recursively process sections
    for section in page.sections:
        text += get_full_page_text(section)

    return text


def wikisummary(query, n_sentence=10):
    wiki = wikipediaapi.Wikipedia('english')
    page = wiki.page(query)

    if not page.exists():
        return "Sorry, I couldn't find information on that."

    # Get full text using the fixed function
    full_text = get_full_page_text(page)

    if not full_text.strip():
        return "No content available for this topic."

    # Original sentences
    sentences = nltk.sent_tokenize(full_text)

    if len(sentences) == 0:
        return "No sentences found in the content."

    # Preprocessing
    cleaned_sentences = [para_processing(s) for s in sentences]

    # TF-IDF and similarity
    tfidf = TfidfVectorizer()
    try:
        tfidf_matrix = tfidf.fit_transform(cleaned_sentences)
        doc_vector = tfidf.transform([" ".join(cleaned_sentences)])
        scores = cosine_similarity(doc_vector, tfidf_matrix).flatten()

        # Pick top sentences
        n_select = min(n_sentence, len(sentences))
        top_indices = scores.argsort()[-n_select:][::-1]

        # Get summary in original order
        summary_sentences = [sentences[i] for i in top_indices]
        summary_sentences.sort(key=lambda x: sentences.index(x))

        return " ".join(summary_sentences)

    except Exception as e:
        return f"Error processing content: {str(e)}"


# Test function
