"""Core models and model infrastructure shared across every app."""

# Python
from typing import Any

# Django
from django.db import models
from django.db.models.base import ModelBase


# ==================================================
# Metaclass
# ==================================================
class BaseModelMeta(ModelBase):
    """Model metaclass that enforces explicit verbose names on concrete ``BaseModel`` children."""

    # ========== constants ==========
    REQUIRED_META_ATTRS = ("verbose_name", "verbose_name_plural")

    def __new__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **kwargs: Any,
    ) -> type:
        """Build the model class, rejecting any concrete child whose Meta omits the
        verbose names."""
        attr_meta = namespace.get("Meta")
        new_class = super().__new__(mcs, name, bases, namespace, **kwargs)
        if new_class._meta.abstract:
            return new_class
        missing = [
            attr
            for attr in mcs.REQUIRED_META_ATTRS
            if getattr(attr_meta, attr, None) is None
        ]
        if missing:
            raise TypeError(
                f"{name} inherits BaseModel and must declare a Meta class with "
                f"{' and '.join(missing)}."
            )
        return new_class


# ==================================================
# Models
# ==================================================
class BaseModel(models.Model, metaclass=BaseModelMeta):
    """Abstract base model adding creation and update timestamps to every model that
    inherits it."""

    # ========== fields ==========
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
