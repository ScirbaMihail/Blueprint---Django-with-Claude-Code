# Project: claude-test

Django project. Local repo, Windows machine, never committed — this file, docs/claude/**, and .claude/settings.json are personal config only.

## Response mode keywords
Every prompt may start with one of these keywords. Detect it and follow the matching mode exactly. If no keyword is present, default to `!CODEBLOCK` behavior.
 
General rule for all modes: minimum viable solution only. No extra abstraction, no speculative options, no defensive code beyond what's asked, no explanatory essays. Solve exactly what was asked, nothing adjacent.
 
- **`!CODE`** — Do not modify files yourself. Output the full content of every affected file in a code block, even if only one line changed. No diffs, no snippets, no explanation beyond a one-line summary per file.
- **`!CODEBLOCK`** — Do not modify files yourself. Output only the changed lines/functions as code blocks, each preceded by the exact file path and location (function name / line range) where it goes. No full files.
- **`!INFO`** — No code, no file edits. Theoretical/explanatory answer only. Keep it as short as the question allows — expand only if explicitly asked to.
- **`!CODE AUTO`** — Modify the files directly using file tools. Reply with a small explanation of what changed — a few lines max, not a report. No full file dumps unless asked.

## Stack
- Python:3.14
- Django:6.1.1
- Django-unfold:0.104.1
- DB: postgresql

## Environment
- Virtualenv: `.venv\Scripts\activate`
- Settings module: `config.settings` for dev
- Env vars in `.env` — never read or print its contents

## Project structure
- `apps/` - one Django app per domain concept
- `config/` - settings package, root urls, wsgi/asgi
- `templates/` - project-level; app templates in `apps/<app>/templates/<app>`
- `static/` - source; `staticfiles` is collectstatic output, never edit directly

## Per-library instructions
Each library/tool has its own file below. Edit each independently as your setup evolves.

@docs/claude/python.md
@docs/claude/django.md
@docs/claude/unfold.md
@docs/claude/git.md

## Security / never touch without asking
- Never print, log or summarize `.env`, `.env.*`, `.gitignore`
- Ask before running `python manage.py makemigrations` and `python manage.py migrate`
- Ask before any destructive DB command (`flush`, `sqlflush`, dropping tables/columns)