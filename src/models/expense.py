from datetime import datetime
from typing import List, Optional
import uuid

class Expense:
    def __init__(self, amount: float, category: str, date: str, description: str):
        self.id = str(uuid.uuid4())
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'date': self.date,
            'description': self.description,
            'created_at': self.created_at
        }
    
    def __str__(self):
        return f"Expense(id={self.id}, amount={self.amount}, category={self.category}, date={self.date})"
