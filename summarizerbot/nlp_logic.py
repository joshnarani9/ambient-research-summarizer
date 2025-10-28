import google.generativeai as genai
import re

# Configure Gemini
genai.configure(api_key="AIzaSyCjH6n0pkmNa7BSJKxhiHURosfzOy5GKoQ")
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_research_summary(text: str) -> str:
    """
    Generates a concise, professional research news summary using Gemini.
    """
    prompt = f"""
You are an expert science journalist AI.
Summarize the following research update into a single paragraph that is engaging,
clear, and accurate. Avoid extra explanations, JSON, or quotes.

Example:
Input: "A new drug has shown promise in treating Alzheimer's by reducing plaque buildup."
Output: "Researchers discovered a promising drug that reduces brain plaque buildup in Alzheimer's, offering hope for early intervention."

Now summarize this:
{text}
"""
    try:
        response = model.generate_content(prompt)
        summary = response.text.strip()
        summary = re.sub(r'(^["\']|["\']$)', '', summary)
        return summary
    except Exception as e:
        return f"⚠️ Unable to summarize right now. ({str(e)})"

