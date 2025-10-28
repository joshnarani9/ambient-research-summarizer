from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from summarizerbot.database import get_all_summaries
from summarizerbot.ambient_agent import start_ambient_loop

app = FastAPI(title="Ambient Research News Summarizer")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def start_background_loop():
    """
    Launch the ambient research summarization loop in the background
    when the app starts.
    """
    start_ambient_loop()
    print("🚀 Ambient agent started (fetches every 5 minutes)")

@app.get("/summaries")
def fetch_all_summaries():
    """
    Returns all stored research summaries.
    """
    return get_all_summaries()
