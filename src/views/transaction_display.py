"""
Transaction Display Module
Provides CLI interface functions for displaying and managing financial transactions.
"""

from src.controllers.spend_controller import SpendController
from typing import Optional
from datetime import datetime


class TransactionDisplay:
    """Handles CLI display and interaction for transaction management."""
    
    def __init__(self):
        self._controller = SpendController()
    
    def create_transaction_interactive(self) -> bool:
        """
        Interactive CLI for creating a new transaction.
        
        Returns:
            True if transaction created successfully, False otherwise
        """
        print("\n=== Add New Transaction ===")
        
        try:
            amount = self._get_amount_input()
            category = self._get_category_input()
            date = self._get_date_input()
            description = self._get_description_input()
            
            transaction = self._controller.add_expense(amount, category, date, description)
            
            if transaction:
                print(f"✓ Transaction recorded successfully!")
                print(f"  ID: {transaction.id[:8]}...")
                print(f"  Amount: ${transaction.amount:.2f}")
                print(f"  Category: {transaction.category}")
                return True
            else:
                print("✗ Failed to create transaction.")
                return False
                
        except ValueError as e:
            print(f"✗ Invalid input: {e}")
            return False
        except KeyboardInterrupt:
            print("\n✗ Operation cancelled.")
            return False
    
    def display_all_transactions(self) -> None:
        """Display all transactions in a formatted table."""
        transactions = self._controller.get_all_expenses()
        
        if not transactions:
            print("\n📭 No transactions found.")
            return
        
        print(f"\n=== All Transactions ({len(transactions)} total) ===")
        print("-" * 90)
        print(f"{'Date':<12} {'Category':<20} {'Amount':>10} {'Description':<40}")
        print("-" * 90)
        
        for txn in transactions:
            description_short = (txn.description[:37] + '...') if len(txn.description) > 40 else txn.description
            print(f"{txn.date:<12} {txn.category:<20} ${txn.amount:>9.2f} {description_short:<40}")
        
        print("-" * 90)
        total = sum(txn.amount for txn in transactions)
        print(f"{'Total:':<32} ${total:>9.2f}")
        print()
    
    def display_filtered_transactions(self) -> None:
        """Interactive CLI for filtering and displaying transactions by category."""
        print("\n=== Filter Transactions ===")
        category = input("Enter category name: ").strip()
        
        if not category:
            print("✗ Category cannot be empty.")
            return
        
        filtered = self._controller.filter_expenses(category=category)
        
        if not filtered:
            print(f"\n📭 No transactions found for category '{category}'.")
            return
        
        print(f"\n=== Transactions in '{category}' ({len(filtered)} found) ===")
        print("-" * 90)
        print(f"{'Date':<12} {'Amount':>10} {'Description':<60}")
        print("-" * 90)
        
        for txn in filtered:
            description_short = (txn.description[:57] + '...') if len(txn.description) > 60 else txn.description
            print(f"{txn.date:<12} ${txn.amount:>9.2f} {description_short:<60}")
        
        print("-" * 90)
        total = sum(txn.amount for txn in filtered)
        print(f"{'Total:':<12} ${total:>9.2f}")
        print()
    
    def _get_amount_input(self) -> float:
        """Get and validate amount input."""
        while True:
            amount_str = input("Amount: $").strip()
            try:
                amount = float(amount_str)
                if amount <= 0:
                    print("  ⚠ Amount must be greater than 0")
                    continue
                return amount
            except ValueError:
                print("  ⚠ Please enter a valid number")
    
    def _get_category_input(self) -> str:
        """Get and validate category input."""
        while True:
            category = input("Category: ").strip()
            if category:
                return category
            print("  ⚠ Category cannot be empty")
    
    def _get_date_input(self) -> str:
        """Get and validate date input."""
        date_input = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
        
        if not date_input:
            return datetime.now().strftime("%Y-%m-%d")
        
        # Validate date format
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            return date_input
        except ValueError:
            print("  ⚠ Invalid date format, using today's date")
            return datetime.now().strftime("%Y-%m-%d")
    
    def _get_description_input(self) -> str:
        """Get description input."""
        description = input("Description: ").strip()
        return description if description else "No description"


# Legacy function wrappers for backward compatibility
_display = TransactionDisplay()

def add_expense_view():
    """Legacy wrapper for add transaction."""
    _display.create_transaction_interactive()

def list_expenses_view():
    """Legacy wrapper for list transactions."""
    _display.display_all_transactions()

def filter_expenses_view():
    """Legacy wrapper for filter transactions."""
    _display.display_filtered_transactions()
