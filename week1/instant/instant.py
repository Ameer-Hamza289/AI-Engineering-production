from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from google import genai

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def instant():
    client = genai.Client()
    message = """
You are on a website that has just been deployed to production for the first time!
Please reply with an enthusiastic announcement to welcome visitors to the site, explaining that it is live on production for the first time!
"""
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=message
    )
    reply = response.text.replace("\n", "<br/>")
    html = f"<html><head><title>Live in an Instant!</title></head><body><p>{reply}</p></body></html>"
    return html