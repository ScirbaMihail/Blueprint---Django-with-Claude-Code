"""
Project default ``ModelAdmin``.

Every admin class in the project extends ``apps.core.admin.ModelAdmin`` instead
of ``unfold.admin.ModelAdmin``. It adds two things on top of Unfold:

1. Permission shortcuts
   ``can_view / can_add / can_change / can_delete(request, model=None, app=None)``
   wrap ``request.user.has_perm("<app>.<action>_<model>")``. With no arguments
   they check the admin's own model; pass ``model``/``app`` to check another one.

2. Declarative changelist tabs
   Declare a ``tabs`` list and each entry becomes a ``?tab=<value>`` view on the
   same changelist, rendered through Unfold's native ``{% tab_list %}`` tag:

       class CustomerAdmin(ModelAdmin):
           tabs = [
               Tab("All"),                                  # no condition -> everything
               Tab("Active", Q(is_active=True)),            # Q object
               Tab("Staff", {"is_staff": True}),            # filter kwargs
               Tab("Recent", lambda qs: qs.order_by("-created")[:100]),
               Tab(
                   "Mine",
                   lambda request, qs: qs.filter(owner=request.user),
                   value="mine",
                   permission=lambda request: request.user.is_authenticated,
               ),
           ]
           # optional (defaults shown):
           # tab_parameter = "tab"
           # tabs_reset_page = True     # drop ?p= when switching tab
           # tabs_show_counts = False   # append "(n)" to every tab label

   The first tab is the default: highlighted and applied when ``?tab=`` is
   missing or unknown. For per-user base scoping that must apply to every tab,
   override ``get_base_queryset`` (not ``get_queryset``) so tab filtering and
   counts stay consistent.
"""

# Python
import inspect
from typing import Any, Callable, Optional, Union

# Django
from django.contrib.admin.views.main import ERROR_FLAG, PAGE_VAR, ChangeList
from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse
from django.utils.text import slugify

# Unfold
from unfold.admin import ModelAdmin as UnfoldModelAdmin


# A tab condition: nothing, a Q, filter kwargs, or a callable returning a queryset.
TabCondition = Union[None, Q, dict, Callable[..., QuerySet]]


# ==================================================
# Helpers
# ==================================================
class Tab:
    """Declarative definition of a single changelist tab."""

    def __init__(
        self,
        title: str,
        condition: TabCondition = None,
        *,
        value: Optional[str] = None,
        permission: Optional[Callable[[HttpRequest], bool]] = None,
        count: Optional[bool] = None,
    ) -> None:
        """
        :param title: Label shown on the tab.
        :param condition: How to narrow the queryset (see module docstring).
        :param value: The ``?tab=`` key. Defaults to ``slugify(title)``.
        :param permission: ``callable(request) -> bool`` gating visibility.
        :param count: Override ``ModelAdmin.tabs_show_counts`` for this tab.
        """
        self.title = title
        self.condition = condition
        self.value = value or slugify(title)
        self.permission = permission
        self.count = count

    def has_permission(self, request: HttpRequest) -> bool:
        if self.permission is None:
            return True
        return bool(self.permission(request))

    def apply(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:
        """Return ``queryset`` narrowed by this tab's condition."""
        condition = self.condition
        if condition is None:
            return queryset
        if isinstance(condition, Q):
            return queryset.filter(condition)
        if isinstance(condition, dict):
            return queryset.filter(**condition)
        if callable(condition):
            return self._call(condition, request, queryset)
        raise TypeError(
            f"Tab {self.value!r}: unsupported condition type {type(condition)!r}. "
            "Use a Q object, a dict of filter kwargs, or a callable."
        )

    @staticmethod
    def _call(func: Callable[..., QuerySet], request: HttpRequest, queryset: QuerySet) -> QuerySet:
        """Call ``func`` as ``(request, queryset)`` or ``(queryset)`` by arity."""
        try:
            positional = [
                p
                for p in inspect.signature(func).parameters.values()
                if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
            ]
            takes_request = len(positional) >= 2
        except (TypeError, ValueError):
            takes_request = True
        return func(request, queryset) if takes_request else func(queryset)


class TabsChangeList(ChangeList):
    """
    ChangeList that hides the ``?tab=`` parameter from Django's lookup handling.

    Django treats every unrecognised query-string key as a model-field lookup.
    Without this, ``?tab=active`` reaches ``queryset.filter(tab="active")``,
    raises ``FieldError``, and Django redirects to ``?e=1``. Removing the key
    from the filter params stops that while keeping it in ``self.params`` so it
    survives across admin actions and preserved filters.
    """

    def get_filters_params(self, params=None):
        lookup_params = super().get_filters_params(params)
        tab_parameter = getattr(self.model_admin, "tab_parameter", "tab")
        lookup_params.pop(tab_parameter, None)
        return lookup_params


# ==================================================
# Admin class
# ==================================================
class ModelAdmin(UnfoldModelAdmin):
    """Project default admin. See module docstring for usage."""

    # ========== Other class attrs ==========
    tabs: list[Tab] = []
    tab_parameter: str = "tab"
    tabs_reset_page: bool = True
    tabs_show_counts: bool = False

    # ========== permissions ==========
    def can_view(self, request: HttpRequest, model: Optional[str] = None, app: Optional[str] = None) -> bool:
        return self._has_perm(request, "view", model, app)

    def can_add(self, request: HttpRequest, model: Optional[str] = None, app: Optional[str] = None) -> bool:
        return self._has_perm(request, "add", model, app)

    def can_change(self, request: HttpRequest, model: Optional[str] = None, app: Optional[str] = None) -> bool:
        return self._has_perm(request, "change", model, app)

    def can_delete(self, request: HttpRequest, model: Optional[str] = None, app: Optional[str] = None) -> bool:
        return self._has_perm(request, "delete", model, app)

    # ========== built-in method overrides ==========
    def get_changelist(self, request: HttpRequest, **kwargs):
        # Keeps ?tab=... out of field-lookup handling (avoids Django's ?e=1 redirect).
        return TabsChangeList

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        queryset = self.get_base_queryset(request)
        # Only filter on the changelist; never on change / delete / autocomplete
        # views, or an object hidden by the default tab would 404.
        if not self._is_changelist_request(request):
            return queryset
        tabs = self.get_visible_tabs(request)
        active = self.get_active_tab(request, tabs)
        if active is None:
            return queryset
        return active.apply(request, queryset)

    def changelist_view(
        self, request: HttpRequest, extra_context: Optional[dict[str, Any]] = None
    ) -> HttpResponse:
        extra_context = dict(extra_context or {})
        tabs = self.get_visible_tabs(request)
        if tabs:
            # Overrides the settings-driven ``tab_list`` for this changelist only;
            # extra_context is merged last, so Unfold's {% tab_list %} renders
            # these items with native styling.
            extra_context["tab_list"] = [self._build_tab_group(request, tabs)]
        return super().changelist_view(request, extra_context)

    # ========== methods ==========
    def get_tabs(self, request: HttpRequest) -> list[Tab]:
        """All declared tabs. Override to build tabs dynamically."""
        return list(self.tabs or [])

    def get_base_queryset(self, request: HttpRequest) -> QuerySet:
        """
        The queryset before any tab condition is applied. Override this (not
        ``get_queryset``) for base scoping so tabs and counts stay consistent.
        """
        return super().get_queryset(request)

    def get_visible_tabs(self, request: HttpRequest) -> list[Tab]:
        return [tab for tab in self.get_tabs(request) if tab.has_permission(request)]

    def get_active_tab(self, request: HttpRequest, tabs: list[Tab]) -> Optional[Tab]:
        """The selected tab, or the first tab as the default."""
        requested = request.GET.get(self.tab_parameter)
        for tab in tabs:
            if tab.value == requested:
                return tab
        return tabs[0] if tabs else None

    def _has_perm(
        self, request: HttpRequest, action: str, model: Optional[str], app: Optional[str]
    ) -> bool:
        app = app.lower() if app else self.model._meta.app_label
        model = model.lower() if model else self.model._meta.model_name
        return request.user.has_perm(f"{app}.{action}_{model}")

    def _build_tab_group(self, request: HttpRequest, tabs: list[Tab]) -> dict[str, Any]:
        active = self.get_active_tab(request, tabs)
        base_queryset: Optional[QuerySet] = None
        items: list[dict[str, Any]] = []

        for tab in tabs:
            title = str(tab.title)
            if self._show_count(tab):
                if base_queryset is None:
                    base_queryset = self.get_base_queryset(request)
                title = f"{title} ({tab.apply(request, base_queryset).count()})"
            items.append(
                {
                    "title": title,
                    "link": self._build_tab_link(request, tab),
                    "active": active is not None and tab.value == active.value,
                    "has_permission": True,  # already filtered in get_visible_tabs
                }
            )

        return {"models": [str(self.opts)], "items": items}

    def _show_count(self, tab: Tab) -> bool:
        return self.tabs_show_counts if tab.count is None else tab.count

    def _build_tab_link(self, request: HttpRequest, tab: Tab) -> str:
        params = request.GET.copy()
        params[self.tab_parameter] = tab.value
        params.pop(ERROR_FLAG, None)  # never carry a stale ?e=1 into tab links
        if self.tabs_reset_page:
            params.pop(PAGE_VAR, None)  # go back to page 1 on tab switch
        query = params.urlencode()
        return f"?{query}" if query else request.path

    def _is_changelist_request(self, request: HttpRequest) -> bool:
        match = getattr(request, "resolver_match", None)
        url_name = getattr(match, "url_name", "") or ""
        return url_name.endswith("_changelist")