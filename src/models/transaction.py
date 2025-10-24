from datetime import datetime
from typing import Optional
import uuid


class Transaction:
    """
    Represents a financial transaction/expense record.
    Tracks spending with amount, category, date, and description.
    """
    
    def __init__(self, amount: float, category: str, date: str, 
                 description: str, transaction_id: Optional[str] = None):
        """
        Create a new transaction record.
        
        Args:
            amount: Transaction amount
            category: Spending category
            date: Transaction date in YYYY-MM-DD format
            description: Transaction description/notes
            transaction_id: Custom identifier (auto-generated if not provided)
        """
        self._id = transaction_id or str(uuid.uuid4())
        self._amount = amount
        self._category = category
        self._date = date
        self._description = description
        self._timestamp = datetime.now().isoformat()
    
    @property
    def id(self) -> str:
        """Get the unique transaction identifier."""
        return self._id
    
    @property
    def amount(self) -> float:
        """Get the transaction amount."""
        return self._amount
    
    @amount.setter
    def amount(self, value: float):
        """Set the transaction amount."""
        self._amount = value
    
    @property
    def category(self) -> str:
        """Get the transaction category."""
        return self._category
    
    @category.setter
    def category(self, value: str):
        """Set the transaction category."""
        self._category = value
    
    @property
    def date(self) -> str:
        """Get the transaction date."""
        return self._date
    
    @date.setter
    def date(self, value: str):
        """Set the transaction date."""
        self._date = value
    
    @property
    def description(self) -> str:
        """Get the transaction description."""
        return self._description
    
    @description.setter
    def description(self, value: str):
        """Set the transaction description."""
        self._description = value
    
    @property
    def created_at(self) -> str:
        """Get the creation timestamp."""
        return self._timestamp
    
    def to_dict(self) -> dict:
        """
        Serialize transaction to dictionary format.
        
        Returns:
            Dictionary containing all transaction attributes
        """
        return {
            'id': self._id,
            'amount': self._amount,
            'category': self._category,
            'date': self._date,
            'description': self._description,
            'created_at': self._timestamp
        }
    
    def __repr__(self) -> str:
        """String representation of transaction."""
        return f"Transaction(id={self._id[:8]}, amount=${self._amount:.2f}, category={self._category}, date={self._date})"
    
    def __str__(self) -> str:
        """User-friendly string representation."""
        return f"${self._amount:.2f} - {self._category} on {self._date}: {self._description}"
