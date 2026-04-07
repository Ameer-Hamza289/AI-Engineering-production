from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from google import genai
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def instant():
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        return (
            "<html><head><title>Live in an Instant!</title></head>"
            "<body><p>Gemini API key is missing. Set GOOGLE_API_KEY (or GEMINI_API_KEY) in your environment.</p></body></html>"
        )

    client = genai.Client(api_key=api_key)
    message = """
You are on a website that has just been deployed to production for the first time!
Please reply with an enthusiastic announcement to welcome visitors to the site, explaining that it is live on production for the first time!
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=message
        )
        reply = (response.text or "").replace("\n", "<br/>")
        if not reply:
            reply = "Site is live, but Gemini returned an empty response."
    except Exception as exc:
        error_text = str(exc)
        if "RESOURCE_EXHAUSTED" in error_text or "429" in error_text:
            reply = (
                "Site is live! Gemini quota is currently exhausted for this key. "
                "Please enable billing or use a key/project with available quota."
            )
        else:
            reply = "Site is live! Gemini is temporarily unavailable. Please try again shortly."

    html = f"<html><head><title>Live in an Instant!</title></head><body><p>{reply}</p></body></html>"
    return html