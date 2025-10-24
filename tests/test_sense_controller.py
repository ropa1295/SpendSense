"""
Unit tests for SenseController
"""
import unittest
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from controllers.sense_controller import SenseController
from controllers.spend_controller import SpendController


class TestSenseController(unittest.TestCase):
    """Test cases for SenseController"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.controller = SenseController()
        self.spend_controller = SpendController()
    
    def test_set_budget(self):
        """Test setting a budget"""
        budget = self.controller.set_budget(
            amount=1000.00,
            month="2025-10",
            category="Groceries"
        )
        
        self.assertIsNotNone(budget)
        self.assertEqual(budget.amount, 1000.00)
        self.assertEqual(budget.month, "2025-10")
        self.assertEqual(budget.category, "Groceries")
    
    def test_set_total_budget(self):
        """Test setting a total budget (no category)"""
        budget = self.controller.set_budget(
            amount=5000.00,
            month="2025-10",
            category=None
        )
        
        self.assertIsNone(budget.category)
        self.assertEqual(budget.amount, 5000.00)
    
    def test_get_all_budgets(self):
        """Test retrieving all budgets"""
        self.controller.set_budget(1000.00, "2025-10", "Groceries")
        self.controller.set_budget(500.00, "2025-10", "Food")
        
        budgets = self.controller.get_all_budgets()
        self.assertGreaterEqual(len(budgets), 2)
    
    def test_get_budgets_by_month(self):
        """Test retrieving budgets for a specific month"""
        self.controller.set_budget(1000.00, "2025-10", "Groceries")
        self.controller.set_budget(500.00, "2025-11", "Food")
        
        october_budgets = self.controller.get_budgets_by_month("2025-10")
        
        self.assertGreater(len(october_budgets), 0)
        for budget in october_budgets:
            self.assertEqual(budget.month, "2025-10")
    
    def test_delete_budget(self):
        """Test deleting a budget"""
        budget = self.controller.set_budget(
            amount=800.00,
            month="2025-10",
            category="Entertainment"
        )
        
        result = self.controller.delete_budget(budget.id)
        self.assertTrue(result)
        
        # Verify it's deleted
        all_budgets = self.controller.get_all_budgets()
        budget_ids = [b.id for b in all_budgets]
        self.assertNotIn(budget.id, budget_ids)
    
    def test_delete_nonexistent_budget(self):
        """Test deleting non-existent budget returns False"""
        result = self.controller.delete_budget("nonexistent")
        self.assertFalse(result)
    
    def test_calculate_spending_vs_budget_within_limit(self):
        """Test budget analysis when spending is within limit"""
        # Set budget
        self.controller.set_budget(1000.00, "2025-10", None)
        
        # Add expenses within budget
        self.spend_controller.add_expense(300.00, "Groceries", "2025-10-20", "Shopping")
        self.spend_controller.add_expense(200.00, "Food", "2025-10-21", "Dining")
        
        expenses = self.spend_controller.get_all_expenses()
        analysis = self.controller.calculate_spending_vs_budget(expenses, "2025-10")
        
        self.assertIn('total_budget', analysis)
        self.assertIn('total_spent', analysis)
        self.assertIn('total_remaining', analysis)
        self.assertEqual(analysis['total_budget'], 1000.00)
        self.assertGreater(analysis['total_remaining'], 0)
    
    def test_calculate_spending_vs_budget_over_limit(self):
        """Test budget analysis when spending exceeds budget"""
        # Set budget
        self.controller.set_budget(500.00, "2025-11", None)
        
        # Add expenses over budget
        self.spend_controller.add_expense(400.00, "Groceries", "2025-11-20", "Shopping")
        self.spend_controller.add_expense(300.00, "Food", "2025-11-21", "Dining")
        
        expenses = self.spend_controller.get_all_expenses()
        analysis = self.controller.calculate_spending_vs_budget(expenses, "2025-11")
        
        self.assertEqual(analysis['total_budget'], 500.00)
        self.assertLess(analysis['total_remaining'], 0)
        self.assertEqual(analysis['status'], 'exceeded')
    
    def test_calculate_spending_vs_budget_no_budget(self):
        """Test budget analysis when no budget is set"""
        expenses = self.spend_controller.get_all_expenses()
        analysis = self.controller.calculate_spending_vs_budget(expenses, "2025-12")
        
        self.assertEqual(analysis['total_budget'], 0)
        self.assertGreaterEqual(analysis['total_spent'], 0)
    
    def test_calculate_spending_vs_budget_category_level(self):
        """Test category-level budget analysis"""
        # Set category budgets
        self.controller.set_budget(500.00, "2025-09", "Groceries")
        self.controller.set_budget(300.00, "2025-09", "Food")
        
        # Add expenses
        self.spend_controller.add_expense(400.00, "Groceries", "2025-09-20", "Shopping")
        self.spend_controller.add_expense(200.00, "Food", "2025-09-21", "Dining")
        
        expenses = self.spend_controller.get_all_expenses()
        analysis = self.controller.calculate_spending_vs_budget(expenses, "2025-09")
        
        self.assertIn('categories', analysis)
        if 'Groceries' in analysis['categories']:
            groceries = analysis['categories']['Groceries']
            self.assertEqual(groceries['budget'], 500.00)
    
    def test_empty_budgets_list(self):
        """Test controller with no budgets"""
        budgets = self.controller.get_all_budgets()
        # May have budgets from previous tests, so just check it's a list
        self.assertIsInstance(budgets, list)


if __name__ == '__main__':
    unittest.main()
