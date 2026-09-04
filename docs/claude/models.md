# Instructions - `models.py` files

## Introduction

All `models.py` files, regardless of which app they belong to, follow one fixed structure. This is non-negotiable — it exists purely to keep every app's models readable and consistent at a glance, not for technical necessity.

## Tech instructions

- Always keep all models in a single `models.py` file, regardless of model count. Never split into `models/` package.
- Every field, class attr, overridden built-in method, and custom method follows the strict declaration order shown below.

## Declaration order

1. **Constants** — plain class-level constants, e.g. `MAX_NAME_LENGTH = 50`
2. **Subclasses** — nested classes, e.g. `TextChoices`/`IntegerChoices` for choice fields
3. **Fields** — anything that's a `models.<Something>Field()`, including FK/M2M/O2O. No subgrouping by field type — one flat group in whatever order makes sense for that model.
4. **Attrs** — everything else that's a class-level assignment but not a field: manager instances (`objects = SomeManager()`), etc.
5. **Properties** — `@property`-decorated methods
6. **`class Meta`**
7. **Overridden built-in methods** — `save()`, `__str__()`, `clean()`, `get_absolute_url()`, etc.
8. **Custom methods** — everything else

## Example

Structural skeleton only — order matters, not the placeholder content.

```python
class MyModel(BaseModel):
    # ========== constants ==========
    MAX_NAME_LENGTH = 50

    # ========== subclasses ==========
    class SomeChoices(models.TextChoices):
        ...

    # ========== fields ==========
    ...

    # ========== attrs ==========
    objects = SomeManager()

    # ========== properties (@property) ==========
    ...

    class Meta:
        verbose_name = "..."
        verbose_name_plural = "..."

    # ========== overridden methods ==========
    ...

    # ========== methods ==========
    ...
```