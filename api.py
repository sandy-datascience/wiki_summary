from fastapi import FastAPI
import uvicorn
from wiki_bot import wikisummary  # Import your func

app = FastAPI()

@app.post("/summarize")
def summarize(query: str, sentences: int = 10):
    summary = wikisummary(query, sentences)
    return {"summary": summary}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)