"""
Legacy expense view module - maintained for backward compatibility.
Redirects to the new transaction_display module.
"""

from src.views.transaction_display import (
    add_expense_view,
    list_expenses_view,
    filter_expenses_view
)

__all__ = ['add_expense_view', 'list_expenses_view', 'filter_expenses_view']
