import google.generativeai as genai
import re
import os

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # ✅ use env var instead of hardcoding
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_research_summary(text: str) -> str:
    """
    Generates a concise, developer-focused research summary using Gemini.
    """

    prompt = f"""
You are an expert AI research communicator helping software developers stay updated
with the latest research and technical advancements.

Summarize the following research update in 2–4 concise sentences that highlight:
1. The core technical contribution or discovery,
2. Its practical or potential application in technology or software,
3. Why it might matter for developers, engineers, or data scientists.

Keep the tone professional, clear, and factual — suitable for inclusion in a
developer Slack channel or internal research feed.

Avoid marketing language, quotes, JSON, or citations. Focus on clarity and usefulness.

Example:
Input:
"A new deep learning model improves code generation accuracy using retrieval-augmented transformers."

Output:
"Researchers developed a retrieval-augmented transformer that significantly improves
code generation accuracy. This approach could enhance developer tools, LLM-based coding
assistants, and automated documentation systems."

Now summarize this:
{text}
"""

    try:
        response = model.generate_content(prompt)
        summary = response.text.strip()

        # Clean any leading/trailing quotes or extra formatting
        summary = re.sub(r'(^["“”\'\s]+|["“”\'\s]+$)', '', summary)
        return summary

    except Exception as e:
        return f"⚠️ Unable to summarize right now. ({str(e)})"
