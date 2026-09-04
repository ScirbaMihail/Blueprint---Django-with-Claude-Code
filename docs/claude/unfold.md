# Unfold and Admin conventions

## Introduction

All admin files, regardless of which app they belong to, follow one fixed structure. This is non-negotiable — it exists purely to keep every app's admin code readable and consistent at a glance, not for technical necessity.

## File structure — always required

There is never a single `admin.py` file. Every app always has an `admin/` directory:

```
<app_label>/admin/
    __init__.py
    <class_name>.py          # one file per admin class, always — even if there's only one
    components/
        forms.py
        filters.py
        fields.py
        widgets.py            # only when needed
        mixins.py             # only when needed
```

Rules:

0. **Base class is always `apps.core.admin.ModelAdmin`** (see `model_admin.md`) — never `unfold.admin.ModelAdmin` or `django.contrib.admin.ModelAdmin` directly.
1. **One admin class per file.** No exceptions, no "just one class so it can live in a shared file." `UserAdmin(ModelAdmin)` → `<app_label>/admin/user_admin.py`. `OrderAdmin(ModelAdmin)` → `<app_label>/admin/order_admin.py`.
2. **`admin/__init__.py`** (the top-level one, not `components/__init__.py`) re-exports every admin class so `admin.site.register` calls (or `@admin.register`) still work cleanly from one import point if needed.
3. **Shared/reusable pieces go in `admin/components/`**, one file per category:
   - `forms.py` — custom `ModelForm`/`Form` classes
   - `filters.py` — custom `SimpleListFilter` or Unfold filter classes
   - `fields.py` — custom form fields
   - `widgets.py` — custom widgets (split out because these tend to accumulate over time)
   - `mixins.py` — shared admin mixins (same reason — grows over time)
   - This list is **open-ended** — add new category files as new kinds of reusable components appear. Don't force something into an existing file just because a new category isn't listed here yet.
   - Naming convention for individual components (classes) inside these files is **not strict** — component variety is too wide to enforce one pattern. Use a name that's clear for that specific case.

## Shared components across apps

`core` is the project-wide utilities app — not admin-specific. Things like `BaseModel` live in `core/models.py` alongside it. Admin components that are reused by more than one app live in `core/components/`, following the same category-file split (`forms.py`, `filters.py`, etc.) as app-local `admin/components/`.

- App-local `admin/components/`: used only within that one app
- `core/components/`: anything imported by 2+ apps
- If a component starts local and later gets reused elsewhere, move it to `core/components/` and update imports — don't leave duplicates

### Import behavior differs between the two

`<app>/admin/components/__init__.py` re-exports everything:
```python
from .forms import *
from .filters import *
...
```
This makes local components importable directly: `from apps.<app>.admin.components import ...`

`core/components/__init__.py` stays **empty**. Core components are always imported explicitly from their category file: `from apps.core.components.filters import ...` — never from the package root.

## Tech instructions

- Every admin class follows the strict declaration order shown in the example below — class attributes, then overridden built-ins, then custom methods, always in that order.
- For iterable class attributes (`list_display`, `fieldsets`, etc.), tuple vs list is not enforced — use whichever fits the case.

## Declaration order reference

The block below is a structural skeleton only — it shows **what goes where and in what order**, not real code. Section comments describe intent where the name alone isn't self-explanatory.

```python
# Imports ...


# ==================================================
# Admin class
# ==================================================
class MyModelAdmin(ModelAdmin):  # apps.core.admin.ModelAdmin
    # ========== Changelist ==========
    tabs = [...]
    list_display = (...)
    list_display_links = (...)
    list_editable = (...)
    search_fields = (...)
    list_filter = (...)
    list_filter_submit = ...
    list_sections = (...)
    actions_list = (...)

    # ========== Changeform ==========
    form = ...
    add_form = ...
    conditional_fields = (...)
    fieldsets = (...)
    add_fieldsets = (...)
    readonly_fields = (...)
    exclude = (...)
    filter_horizontal = (...)
    inlines = (...)
    actions_detail = (...)

    # ========== Other class attrs (e.g. Media) ==========
    class Media:
        ...

    # ========== @display and @action decorated methods ==========
    ...

    # ========== permissions (has_*_permission overrides) ==========
    ...

    # ========== built-in method overrides ==========
    get_urls()
    get_queryset()
    get_list_display()
    get_fieldsets()
    get_readonly_fields()
    get_exclude()

    # ========== custom methods ==========
    ...
```