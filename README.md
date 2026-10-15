# hga-demo

A tiny todo app — a FastAPI JSON API and a single HTML page — that exists to try the
[hga Claude Code plugin](https://github.com/hgahub/claude-plugins) on: its issues are real, small and
reproducible, so `/hga:triage` and `/hga:issue` can take them from triage to a reviewed pull request.

```
uv sync
uv run pytest -q
uv run uvicorn app:app --port 8000      # http://localhost:8000/
```

The data lives in memory and resets on every restart.

## License

[MIT](LICENSE)
