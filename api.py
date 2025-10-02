from fastapi import FastAPI
from wiki_bot import wikisummary
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Wikipedia Summarizer API is running!"}

@app.post("/summarize")
def summarize(query: str, sentences: int = 10):
    summary = wikisummary(query, sentences)
    return {"summary": summary}