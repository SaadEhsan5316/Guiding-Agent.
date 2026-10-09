import os

from dotenv import load_dotenv
import html

import markdown
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing. Add it to your .env file.")

# The Groq client (this is the part that was missing last time)
client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = """You are a professional, highly experienced career guide and mentor.
The user will give you the name of their degree.
Give a practical roadmap of the courses they should do to build a strong career efficiently:

1. Core degree courses that matter most (and why).
2. Important courses/skills OUTSIDE the degree that employers value in this field.
3. Recommended order: Beginner -> Intermediate -> Advanced.
4. Free or paid platforms to learn them (Coursera, YouTube, edX, etc.).
5. Short final advice: projects, certifications, and next steps.

Be concise, honest and practical. Use clear headings and bullet points."""

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Career Guide: __DEGREE__</title>
<style>
  :root { --bg:#f5f7fb; --card:#fff; --text:#1f2937; --muted:#6b7280;
          --accent:#4f46e5; --line:#e5e7eb; --head:#eef2ff; }
  @media (prefers-color-scheme: dark) {
    :root { --bg:#0f172a; --card:#1e293b; --text:#e5e7eb; --muted:#94a3b8;
            --accent:#818cf8; --line:#334155; --head:#273449; }
  }
  * { box-sizing: border-box; }
  body { margin:0; background:var(--bg); color:var(--text);
         font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
         line-height:1.6; }
  header { background:var(--accent); color:#fff; padding:28px 16px; text-align:center; }
  header h1 { margin:0; font-size:1.6rem; }
  header p { margin:6px 0 0; opacity:.85; }
  main { max-width:960px; margin:24px auto; padding:0 16px 48px; }
  .card { background:var(--card); border:1px solid var(--line); border-radius:14px;
          padding:8px 24px 24px; box-shadow:0 2px 10px rgba(0,0,0,.05); }
  h2 { color:var(--accent); margin-top:32px; padding-bottom:8px;
       border-bottom:2px solid var(--line); font-size:1.3rem; }
  .tw { overflow-x:auto; margin:14px 0; }
  table { border-collapse:collapse; width:100%; font-size:.93rem; }
  th, td { border:1px solid var(--line); padding:10px 12px; text-align:left; vertical-align:top; }
  th { background:var(--head); }
  tr:nth-child(even) td { background:rgba(127,127,127,.05); }
  blockquote { margin:14px 0; padding:10px 16px; border-left:4px solid var(--accent);
               background:var(--head); border-radius:6px; }
  hr { border:none; border-top:1px solid var(--line); margin:24px 0; }
  li { margin:6px 0; }
  a { color:var(--accent); }
</style>
</head>
<body>
<header>
  <h1>Career Roadmap: __DEGREE__</h1>
  <p>Your personalised course guide</p>
</header>
<main><div class="card">__CONTENT__</div></main>
</body>
</html>"""

app = FastAPI(title="Degree Career Guide Agent")


def run_agent(degree: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"My degree is: {degree}"},
        ],
        temperature=0.6,
    )
    return response.choices[0].message.content


@app.get("/")
def home():
    return {"message": "Use /guide/{your degree}, e.g. /guide/Computer Science"}


@app.get("/guide/{degree}", response_class=HTMLResponse)
def guide(degree: str):
    try:
        answer = run_agent(degree)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq error: {e}")

    # Convert the markdown answer into a nicely styled web page
    body = markdown.markdown(answer, extensions=["tables", "sane_lists"])
    body = body.replace("<table>", '<div class="tw"><table>').replace(
        "</table>", "</table></div>"
    )
    page = PAGE.replace("__DEGREE__", html.escape(degree)).replace("__CONTENT__", body)
    return HTMLResponse(page)