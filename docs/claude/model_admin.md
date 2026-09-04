# Default `ModelAdmin` — `apps/core/admin/model_admin.py`

Every admin class in the project extends this, never `unfold.admin.ModelAdmin` directly:

```python
from apps.core.admin import ModelAdmin, Tab
```

It is a drop-in Unfold `ModelAdmin` with two additions.

## 1. Permission shortcuts

Use these instead of `request.user.has_perm("app.action_model")` inside admin methods:

| Method | Checks |
|---|---|
| `self.can_view(request)` | `<app>.view_<model>` |
| `self.can_add(request)` | `<app>.add_<model>` |
| `self.can_change(request)` | `<app>.change_<model>` |
| `self.can_delete(request)` | `<app>.delete_<model>` |

- With no extra args they check the admin's own model.
- Pass `model="order"` and/or `app="shop"` to check another model. Both are lowercased automatically.
- These are helpers for use *inside* your own logic (e.g. `get_readonly_fields`, `@action`). They do **not** replace Django's `has_view_permission` etc. — override those as usual when you need to change admin-level access.

## 2. Declarative changelist tabs

Declare `tabs` on the admin class; each entry becomes a `?tab=<value>` view of the same changelist, rendered with native Unfold tab styling.

```python
class CustomerAdmin(ModelAdmin):
    tabs = [
        Tab("All"),                                     # no condition
        Tab("Active", Q(is_active=True)),               # Q object
        Tab("Staff", {"is_staff": True}),               # filter kwargs
        Tab("Recent", lambda qs: qs.order_by("-created")[:100]),
        Tab(
            "Mine",
            lambda request, qs: qs.filter(owner=request.user),
            value="mine",                               # ?tab= key (default: slugify(title))
            permission=lambda request: request.user.is_superuser,
            count=True,                                 # per-tab override of tabs_show_counts
        ),
    ]
```

`Tab(title, condition=None, *, value=None, permission=None, count=None)`

Condition can be `None`, a `Q`, a dict of filter kwargs, `callable(qs)`, or `callable(request, qs)`.

Class knobs (defaults):
- `tab_parameter = "tab"` — query-string key
- `tabs_reset_page = True` — drop `?p=` when switching tab
- `tabs_show_counts = False` — append `(n)` to every tab label (one extra `COUNT` query per tab)

Rules:
- First tab is the default — active when `?tab=` is missing or unknown. Make it the "All"/broadest one.
- Tab filtering applies **only** to the changelist; change/delete/autocomplete views see the full queryset, so objects hidden by the default tab still open.
- For base scoping that must apply to every tab (per-user data, soft-delete), override `get_base_queryset`, **not** `get_queryset`. Overriding `get_queryset` bypasses tab filtering and breaks counts.
- Dynamic tabs: override `get_tabs(request)` and return a list of `Tab`.

## Where things live
- `apps/core/admin/model_admin.py` — `ModelAdmin`, plus its helpers `Tab` and `TabsChangeList`
- `apps/core/admin/__init__.py` re-exports `ModelAdmin` and `Tab`