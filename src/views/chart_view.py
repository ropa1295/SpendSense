"""
Legacy chart view module - maintained for backward compatibility.
Redirects to the new visual_analytics module.
"""

from src.views.visual_analytics import generate_expense_chart

__all__ = ['generate_expense_chart']
