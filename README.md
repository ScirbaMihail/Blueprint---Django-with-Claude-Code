# Django + Claude Code Blueprint

A Django starter project for anyone who wants to skip the initial setup grind — and comes pre-configured for [Claude Code](https://docs.claude.com/en/docs/claude-code/overview), so AI-assisted development follows your project's conventions instead of fighting them.

## Stack

- **Django** — web framework
- **[django-unfold](https://unfoldadmin.com/docs/installation/quickstart/)** — modern admin theme/toolkit ([demo](https://demo.unfoldadmin.com/en/admin/login/))
- **psycopg2-binary** — PostgreSQL adapter

## Why the Claude configuration matters

Claude Code, unconfigured, tends to overthink simple tasks, add code you didn't ask for, and ignore your project's conventions. This repo ships with configuration that fixes that — so if you use Claude Code, it follows this project's structure and conventions instead of inventing its own.

If you don't use Claude Code, ignore this section entirely — the project runs the same either way.

- **`CLAUDE.md`** — root-level instructions Claude applies regardless of what part of the project it's touching (response style, stack overview, security rules)
- **`docs/claude/*.md`** — one file per library/topic (Django models, admin/Unfold conventions, testing, git, etc.), imported from `CLAUDE.md`
- **`.claude/settings.json`** — tool permissions (safe commands auto-allowed, sensitive files like `.env` blocked from being read)

These files double as project documentation even if you never touch Claude Code — they describe the conventions this project expects, so read through `docs/claude/*.md` to understand how the codebase is organized before contributing.

## Setup

This is meant to be downloaded once and turned into your own project with its own git history — not cloned/forked as a live fork of this repo.

1. Download this repo as a ZIP and extract it into your new project folder.
2. `git init` and create a new repository on GitHub, then link it as your remote.
3. **If you don't want the Claude configuration in your repo**, add to `.gitignore` before your first commit:
   ```gitignore
   CLAUDE.md
   .claude/
   docs/claude/
   ```
   Otherwise, keep them — they're safe to share and useful as living documentation for contributors.
4. Create a Python virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create a `.env` file in the project root:
   ```env
   # Django
   DJANGO_SECRET_KEY=
   DJANGO_DEBUG=
   DJANGO_ALLOWED_HOSTS=

   # Database
   DB_NAME=
   DB_USER=
   DB_PASSWORD=
   DB_HOST=
   DB_PORT=
   ```
   Fill in real values — `DJANGO_SECRET_KEY` should be a fresh, unique value per project, never reused from this README or another project.
6. Run migrations and start the dev server as usual (`python manage.py migrate`, `python manage.py runserver`).

## Using Claude Code with this project

1. Install the [Claude Code extension](https://docs.claude.com/en/docs/claude-code/vs-code) for VS Code and sign in.
2. Open the project folder — `CLAUDE.md` loads automatically at the start of every session, no setup needed.
3. Adjust `CLAUDE.md` and `docs/claude/*.md` freely as your project's conventions evolve; they're plain Markdown, not fixed rules from this template.

## License

No license file yet — treat this as "use freely for your own projects" in the meantime; a formal license may be added later.