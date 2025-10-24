"""
Unit tests for Transaction model
"""
import unittest
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from models.transaction import Transaction
from datetime import datetime


class TestTransaction(unittest.TestCase):
    """Test cases for Transaction model"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.transaction = Transaction(
            amount=50.99,
            category="Groceries",
            date="2025-10-24",
            description="Weekly shopping"
        )
    
    def test_transaction_creation(self):
        """Test transaction is created with correct attributes"""
        self.assertIsNotNone(self.transaction.id)
        self.assertEqual(self.transaction.amount, 50.99)
        self.assertEqual(self.transaction.category, "Groceries")
        self.assertEqual(self.transaction.date, "2025-10-24")
        self.assertEqual(self.transaction.description, "Weekly shopping")
        self.assertIsNotNone(self.transaction.created_at)
    
    def test_transaction_id_is_unique(self):
        """Test that each transaction gets a unique ID"""
        transaction2 = Transaction(
            amount=25.00,
            category="Food",
            date="2025-10-24",
            description="Lunch"
        )
        self.assertNotEqual(self.transaction.id, transaction2.id)
    
    def test_transaction_to_dict(self):
        """Test transaction can be converted to dictionary"""
        transaction_dict = self.transaction.to_dict()
        
        self.assertIsInstance(transaction_dict, dict)
        self.assertEqual(transaction_dict['amount'], 50.99)
        self.assertEqual(transaction_dict['category'], "Groceries")
        self.assertEqual(transaction_dict['date'], "2025-10-24")
        self.assertEqual(transaction_dict['description'], "Weekly shopping")
        self.assertIn('id', transaction_dict)
        self.assertIn('created_at', transaction_dict)
    
    def test_transaction_amount_modification(self):
        """Test transaction amount can be modified"""
        self.transaction.amount = 75.50
        self.assertEqual(self.transaction.amount, 75.50)
    
    def test_transaction_category_modification(self):
        """Test transaction category can be modified"""
        self.transaction.category = "Food"
        self.assertEqual(self.transaction.category, "Food")
    
    def test_transaction_date_modification(self):
        """Test transaction date can be modified"""
        self.transaction.date = "2025-10-25"
        self.assertEqual(self.transaction.date, "2025-10-25")
    
    def test_transaction_description_modification(self):
        """Test transaction description can be modified"""
        self.transaction.description = "Monthly groceries"
        self.assertEqual(self.transaction.description, "Monthly groceries")
    
    def test_transaction_with_minimal_data(self):
        """Test transaction with only required fields"""
        minimal_transaction = Transaction(
            amount=10.00,
            category="Other",
            date="2025-10-24",
            description=""
        )
        self.assertIsNotNone(minimal_transaction.id)
        self.assertEqual(minimal_transaction.description, "")
    
    def test_transaction_properties_are_read_only(self):
        """Test that id and created_at cannot be directly modified"""
        with self.assertRaises(AttributeError):
            self.transaction.id = "new-id"
        
        with self.assertRaises(AttributeError):
            self.transaction.created_at = "2025-01-01"


if __name__ == '__main__':
    unittest.main()
