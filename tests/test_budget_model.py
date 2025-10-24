"""
Unit tests for BudgetPlan model
"""
import unittest
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from models.budget_plan import BudgetPlan


class TestBudgetPlan(unittest.TestCase):
    """Test cases for BudgetPlan model"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.budget = BudgetPlan(
            amount=1000.00,
            month="2025-10",
            category="Groceries"
        )
    
    def test_budget_creation(self):
        """Test budget is created with correct attributes"""
        self.assertIsNotNone(self.budget.id)
        self.assertEqual(self.budget.amount, 1000.00)
        self.assertEqual(self.budget.month, "2025-10")
        self.assertEqual(self.budget.category, "Groceries")
        self.assertIsNotNone(self.budget.created_at)
    
    def test_budget_creation_without_category(self):
        """Test budget can be created without category (total budget)"""
        total_budget = BudgetPlan(
            amount=5000.00,
            month="2025-10",
            category=None
        )
        self.assertIsNone(total_budget.category)
        self.assertEqual(total_budget.amount, 5000.00)
    
    def test_budget_id_is_unique(self):
        """Test that each budget gets a unique ID"""
        budget2 = BudgetPlan(
            amount=500.00,
            month="2025-10",
            category="Food"
        )
        self.assertNotEqual(self.budget.id, budget2.id)
    
    def test_budget_to_dict(self):
        """Test budget can be converted to dictionary"""
        budget_dict = self.budget.to_dict()
        
        self.assertIsInstance(budget_dict, dict)
        self.assertEqual(budget_dict['amount'], 1000.00)
        self.assertEqual(budget_dict['month'], "2025-10")
        self.assertEqual(budget_dict['category'], "Groceries")
        self.assertIn('id', budget_dict)
        self.assertIn('created_at', budget_dict)
    
    def test_budget_to_dict_with_none_category(self):
        """Test budget with None category converts properly"""
        total_budget = BudgetPlan(
            amount=5000.00,
            month="2025-10",
            category=None
        )
        budget_dict = total_budget.to_dict()
        self.assertIsNone(budget_dict['category'])
    
    def test_budget_properties_are_immutable(self):
        """Test that certain budget properties cannot be modified"""
        # Test that month property is read-only (no setter)
        with self.assertRaises(AttributeError):
            self.budget.month = "2025-12"
        
        # Note: amount property HAS a setter, so it can be modified
        # This is by design to allow budget adjustments
        self.budget.amount = 2000.00
        self.assertEqual(self.budget.amount, 2000.00)
        
        with self.assertRaises(AttributeError):
            self.budget.month = "2025-11"
        
        with self.assertRaises(AttributeError):
            self.budget.category = "Food"
    
    def test_budget_id_immutable(self):
        """Test that id cannot be modified"""
        with self.assertRaises(AttributeError):
            self.budget.id = "new-id"
    
    def test_budget_created_at_immutable(self):
        """Test that created_at cannot be modified"""
        with self.assertRaises(AttributeError):
            self.budget.created_at = "2025-01-01"


if __name__ == '__main__':
    unittest.main()
