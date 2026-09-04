# Django conventions

## Commands
- Run server: `python manage.py runserver`
- Make migrations: `python manage.py makemigrations`
- Migrate: `python manage.py migrate`
- Shell: `python manage.py shell`
- Create superuser: `python manage.py createsuperuser`

## Architecture
- Business logic goes in `services.py` or model methods, not in views
- Prefer ORM `select_related`/`prefetch_related` over raw SQL; raw SQL needs a comment explaining why
- One migration per logical change - don't squash unrelated model changes into one migration file

## Models
The models convention has its own file. 
@docs/claude/models.md

## URLs
- Each app has its own `urls.py` included by root urls
- Each `include()` in root urls has its own namespace.

## Admin
The admin convention has its own file
@docs/claude/unfold.md

## Django settings module
The django settings module convention has its own file
@docs/claude/django_settings.md