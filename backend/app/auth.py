"""
Compatibility module for legacy imports.

Several routes import auth helpers from ``app.auth``.
The actual implementation lives in ``app.services.auth``.
"""

from .services.auth import get_current_teacher, get_current_user

__all__ = ["get_current_user", "get_current_teacher"]
