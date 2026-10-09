# Guiding Agent

An AI career guide built with **FastAPI** and the **Groq API**. Type your degree name in the URL, and the agent acts as an experienced career mentor: it lists the courses you should take, both from within your degree and beyond it, to build your career efficiently.

## What It Does

- Takes a degree name from the URL (e.g. `/guide/Computer Science`)
- Sends it to a Groq-hosted LLM with a career-mentor system prompt
- Returns a structured roadmap as a clean, readable web page:
  1. Core degree courses that matter most
  2. High-value skills and courses outside the degree
  3. Learning path: Beginner, Intermediate, Advanced
  4. Platforms to learn from (free and paid)
  5. Final actionable advice (projects, certifications, next steps)

## Tech Stack

| Tool | Purpose |
|------|---------|
| FastAPI | Web framework / API |
| Uvicorn | Server |
| Groq | LLM inference (`openai/gpt-oss-120b`) |
| python-dotenv | Loads the API key from `.env` |
| Markdown | Converts the AI answer into HTML |
| uv | Package and environment manager |

## Getting Started

### 1. Clone the repository

```
git clone https://github.com/SaadEhsan5316/Guiding-Agent.git
cd Guiding-Agent
```

### 2. Install dependencies

```
uv sync
```

### 3. Add your API key

Get a free key from [console.groq.com](https://console.groq.com), then create a `.env` file in the project folder:

```
GROQ_API_KEY=your_key_here
```

(See `.env.example` for the format.)

### 4. Run the server

```
uv run uvicorn main:app --reload
```

### 5. Open in your browser

```
http://127.0.0.1:8000/guide/Computer Science
```

Change the degree name in the URL to get a roadmap for any field, e.g. `/guide/Agriculture` or `/guide/Software Engineering`.

## Project Structure

```
Guiding-Agent/
├── main.py          # FastAPI app + Groq agent
├── pyproject.toml   # Dependencies (uv)
├── uv.lock          # Locked versions
├── .env.example     # Example environment file
└── README.md
```

## Notes

- Never commit your real `.env` file. It is listed in `.gitignore`.
- If the model name stops working, check the current list at [console.groq.com/docs/models](https://console.groq.com/docs/models) and update `MODEL` in `main.py`.

## Author

Saad Ehsan: [@SaadEhsan5316](https://github.com/SaadEhsan5316)
