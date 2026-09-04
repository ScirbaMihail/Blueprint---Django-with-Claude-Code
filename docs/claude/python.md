# Python conventions
- Type hints required on new functions and methods
- Docstrings on all methods with non-trivial logic
- Prefer f-strings over `.format()` or `%`
- Imports ordered with respective comments - look at **Imports** section bellow

## Dependency management
- `pip install*` is pre-approved for this session
- After adding a package: update `requirements.txt`. Add only target-package name, without auto-installed packages. 
  E.g. `Django==<version>` instead of `Django==<version> asgiref==<version>`

## Imports
- Ordering: python, django, unfold, third-party, local
- Comments each section. If there are no import for the section, skip it at all including comment.
  Look at the example bellow:
  ```python
  # Python
  ...
  # Django
  ...
  # Unfold
  ...
  # Third-party
  ...
  # Local
  ...
  ```
- Additional ordering: order alphabetically
  Look at the example bellow:
  ```python
  # Django
  from django.contrib import auth
  from django.contrib.admin import ModelAdmin
  from django.contrib.auth import get_user_model
  from django.db.models import Q
  ...
  ```