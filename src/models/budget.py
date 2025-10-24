from datetime import datetime
from typing import Optional
import uuid

class Budget:
    def __init__(self, amount: float, month: str, category: Optional[str] = None, budget_id: Optional[str] = None):
        """
        Initialize a Budget instance
        
        Args:
            amount: Budget amount
            month: Month in YYYY-MM format
            category: Optional category for budget (None for total budget)
            budget_id: Optional custom ID
        """
        self.id = budget_id or str(uuid.uuid4())
        self.amount = amount
        self.month = month  # Format: YYYY-MM
        self.category = category  # None means total budget for the month
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        """Convert budget to dictionary"""
        return {
            'id': self.id,
            'amount': self.amount,
            'month': self.month,
            'category': self.category,
            'created_at': self.created_at
        }
    
    def __repr__(self):
        category_str = f" ({self.category})" if self.category else ""
        return f"Budget{category_str}: ${self.amount} for {self.month}"