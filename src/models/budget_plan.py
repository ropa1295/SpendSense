from datetime import datetime
from typing import Optional
import uuid


class BudgetPlan:
    """
    Represents a financial budget allocation for tracking spending limits.
    Supports both overall monthly budgets and category-specific allocations.
    """
    
    def __init__(self, amount: float, month: str, category: Optional[str] = None, 
                 budget_id: Optional[str] = None):
        """
        Create a new budget plan instance.
        
        Args:
            amount: Budget allocation amount
            month: Target month in YYYY-MM format
            category: Specific category (None for overall monthly budget)
            budget_id: Custom identifier (auto-generated if not provided)
        """
        self._id = budget_id or str(uuid.uuid4())
        self._amount = amount
        self._month = month
        self._category = category
        self._timestamp = datetime.now().isoformat()
    
    @property
    def id(self) -> str:
        """Get the unique budget identifier."""
        return self._id
    
    @property
    def amount(self) -> float:
        """Get the budget amount."""
        return self._amount
    
    @amount.setter
    def amount(self, value: float):
        """Set the budget amount."""
        self._amount = value
    
    @property
    def month(self) -> str:
        """Get the target month."""
        return self._month
    
    @property
    def category(self) -> Optional[str]:
        """Get the budget category."""
        return self._category
    
    @property
    def created_at(self) -> str:
        """Get the creation timestamp."""
        return self._timestamp
    
    def to_dict(self) -> dict:
        """
        Serialize budget plan to dictionary format.
        
        Returns:
            Dictionary containing all budget attributes
        """
        return {
            'id': self._id,
            'amount': self._amount,
            'month': self._month,
            'category': self._category,
            'created_at': self._timestamp
        }
    
    def __repr__(self) -> str:
        """String representation of budget plan."""
        category_label = f" [{self._category}]" if self._category else " [Overall]"
        return f"BudgetPlan{category_label}: ${self._amount:.2f} for {self._month}"
    
    def __str__(self) -> str:
        """User-friendly string representation."""
        return self.__repr__()
