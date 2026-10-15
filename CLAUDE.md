# hga-demo

A tiny FastAPI todo app used to try the hga Claude Code plugin. Keep it small.

- Install: `uv sync`
- Gate before a PR: `uv run pytest -q` (all green)
- Run: `uv run uvicorn app:app --port 8000` — the page is at `/`, the API under `/api/todos`
- Settings come from the environment (`.env`, see `.env.example`); the data is in memory and resets on restart
- In the browser, `window.state` holds the current filter and the loaded todos
- Commit messages: `fix(#<n>): …` / `feat(#<n>): …`, in English
