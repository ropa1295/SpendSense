from typing import List, Optional, Dict, Any
import csv
import io
from datetime import datetime
from models.expense import Expense

class SpendController:
    """
    Manages expense tracking and financial transaction records.
    Handles CRUD operations, filtering, and data export for spending analysis.
    """
    
    def __init__(self):
        self._expense_ledger: List[Expense] = []
    
    def add_expense(self, amount: float = None, category: str = None, date: str = None, 
                   description: str = None) -> Optional[Expense]:
        """
        Record a new expense transaction.
        Supports both programmatic and CLI interactive modes.
        
        Args:
            amount: Transaction amount (None triggers CLI mode)
            category: Expense category
            date: Transaction date in YYYY-MM-DD format
            description: Expense description
            
        Returns:
            Created Expense instance or None if creation fails
        """
        # Interactive CLI mode when no amount provided
        if amount is None:
            expense_data = self._gather_expense_from_cli()
            if not expense_data:
                return None
            amount, category, date, description = expense_data
        
        # Create and register new expense
        new_expense = Expense(amount, category, date, description)
        self._expense_ledger.append(new_expense)
        
        return new_expense
    
    def _gather_expense_from_cli(self) -> Optional[tuple]:
        """
        Interactive CLI helper to gather expense details from user input.
        
        Returns:
            Tuple of (amount, category, date, description) or None on error
        """
        try:
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            
            date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
            date = date_input if date_input else datetime.now().strftime("%Y-%m-%d")
            
            description = input("Enter description: ")
            
            print(f"Expense recorded successfully!")
            return (amount, category, date, description)
            
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            return None
        except Exception as error:
            print(f"Error collecting input: {error}")
            return None
    
    def get_all_expenses(self) -> List[Expense]:
        """
        Retrieve complete collection of all recorded expenses.
        
        Returns:
            List of all Expense instances
        """
        return list(self._expense_ledger)
    
    def list_expenses(self):
        """Display all expenses in CLI-friendly format."""
        if not self._expense_ledger:
            print("No expenses found.")
            return
        
        print("\n--- All Expenses ---")
        for record in self._expense_ledger:
            print(f"ID: {record.id[:8]}... | Amount: ${record.amount} | "
                  f"Category: {record.category} | Date: {record.date} | "
                  f"Description: {record.description}")
    
    def get_expense_by_id(self, expense_id: str) -> Optional[Expense]:
        """
        Locate a specific expense by its unique identifier.
        Supports both full ID and partial ID prefix matching.
        
        Args:
            expense_id: Full or partial expense ID
            
        Returns:
            Matching Expense instance or None if not found
        """
        return self._search_expense_by_id(expense_id)
    
    def _search_expense_by_id(self, expense_id: str) -> Optional[Expense]:
        """Internal helper for ID-based expense lookup."""
        for record in self._expense_ledger:
            if record.id == expense_id or record.id.startswith(expense_id):
                return record
        return None
    
    def edit_expense(self):
        """
        Interactive CLI mode for modifying an existing expense.
        Prompts user for expense ID and new values for each field.
        """
        expense_id = input("Enter expense ID to edit: ")
        target_expense = self._search_expense_by_id(expense_id)
        
        if not target_expense:
            print("Expense not found.")
            return
        
        print(f"Current expense: {target_expense}")
        
        try:
            # Gather updated values with defaults to current values
            updated_data = self._gather_update_data(target_expense)
            
            # Apply updates
            self.update_expense(
                target_expense.id,
                amount=updated_data['amount'],
                category=updated_data['category'],
                date=updated_data['date'],
                description=updated_data['description']
            )
            print("Expense updated successfully!")
            
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
        except Exception as error:
            print(f"Error updating expense: {error}")
    
    def _gather_update_data(self, current_expense: Expense) -> Dict[str, Any]:
        """Helper to collect updated expense data from CLI."""
        amount_input = input(f"Enter new amount (current: {current_expense.amount}): ")
        amount = float(amount_input) if amount_input else current_expense.amount
        
        category = input(f"Enter new category (current: {current_expense.category}): ") or current_expense.category
        date = input(f"Enter new date (current: {current_expense.date}): ") or current_expense.date
        description = input(f"Enter new description (current: {current_expense.description}): ") or current_expense.description
        
        return {
            'amount': amount,
            'category': category,
            'date': date,
            'description': description
        }
    
    def update_expense(self, expense_id: str, amount: float = None, category: str = None, 
                      date: str = None, description: str = None) -> Optional[Expense]:
        """
        Modify an existing expense with new values.
        Only updates fields that are explicitly provided (not None).
        
        Args:
            expense_id: Unique identifier of expense to update
            amount: New amount (optional)
            category: New category (optional)
            date: New date (optional)
            description: New description (optional)
            
        Returns:
            Updated Expense instance or None if not found
        """
        target_expense = self._search_expense_by_id(expense_id)
        
        if not target_expense:
            return None
        
        # Apply updates only for provided fields
        if amount is not None:
            target_expense.amount = amount
        if category is not None:
            target_expense.category = category
        if date is not None:
            target_expense.date = date
        if description is not None:
            target_expense.description = description
            
        return target_expense
    
    def delete_expense(self, expense_id: str = None) -> bool:
        """
        Remove an expense from the ledger.
        Supports both programmatic and interactive CLI modes.
        
        Args:
            expense_id: Unique identifier (None triggers CLI mode)
            
        Returns:
            True if deletion successful, False if expense not found
        """
        # CLI mode when no ID provided
        cli_mode = expense_id is None
        if cli_mode:
            expense_id = input("Enter expense ID to delete: ")
        
        target_expense = self._search_expense_by_id(expense_id)
        
        if target_expense:
            self._expense_ledger.remove(target_expense)
            if cli_mode:
                print("Expense deleted successfully!")
            return True
        else:
            if cli_mode:
                print("Expense not found.")
            return False
    
    def filter_expenses(self, category: str = None, date_from: str = None, 
                       date_to: str = None, tag: str = None) -> List[Expense]:
        """
        Filter expenses based on various criteria.
        Supports both programmatic filtering and interactive CLI mode.
        
        Args:
            category: Filter by category name
            date_from: Filter by start date
            date_to: Filter by end date
            tag: Filter by tag (deprecated, kept for compatibility)
            
        Returns:
            List of expenses matching the filter criteria
        """
        # Check if CLI mode (all parameters are None)
        cli_mode = all(param is None for param in [category, date_from, date_to, tag])
        
        if cli_mode:
            category, _ = self._gather_filter_criteria()
        
        # Start with full ledger and apply filters
        filtered_results = list(self._expense_ledger)
        
        if category:
            filtered_results = self._filter_by_category(filtered_results, category)
        
        # Display results in CLI mode
        if cli_mode:
            self._display_filtered_results(filtered_results)
        
        return filtered_results
    
    def _gather_filter_criteria(self) -> tuple:
        """Helper to collect filter criteria from CLI."""
        print("Filter options:")
        category = input("Enter category (or press Enter to skip): ") or None
        return category, None
    
    def _filter_by_category(self, expenses: List[Expense], category: str) -> List[Expense]:
        """Helper to filter expenses by category (case-insensitive)."""
        return [exp for exp in expenses if exp.category.lower() == category.lower()]
    
    def _display_filtered_results(self, filtered: List[Expense]):
        """Helper to display filtered results in CLI mode."""
        if not filtered:
            print("No expenses found matching the criteria.")
            return
        
        print(f"\n--- Filtered Expenses ({len(filtered)} found) ---")
        for record in filtered:
            print(f"ID: {record.id[:8]}... | Amount: ${record.amount} | "
                  f"Category: {record.category} | Date: {record.date}")
    
    def export_to_csv(self) -> str:
        """
        Generate CSV export of all expenses.
        
        Returns:
            String containing CSV-formatted expense data
        """
        return self._generate_csv_output()
    
    def _generate_csv_output(self) -> str:
        """Internal helper to create CSV export."""
        buffer = io.StringIO()
        csv_writer = csv.writer(buffer)
        
        # Write header row
        header_columns = ['ID', 'Amount', 'Category', 'Date', 'Description', 'Created At']
        csv_writer.writerow(header_columns)
        
        # Write expense records
        for record in self._expense_ledger:
            row_data = [
                record.id,
                record.amount,
                record.category,
                record.date,
                record.description,
                record.created_at
            ]
            csv_writer.writerow(row_data)
        
        # Extract CSV content and cleanup
        csv_content = buffer.getvalue()
        buffer.close()
        
        return csv_content
