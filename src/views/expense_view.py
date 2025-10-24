from src.controllers.spend_controller import SpendController

spend_controller = SpendController()

def add_expense_view():
    amount = float(input("Enter amount: "))
    category = input("Enter category: ")
    date = input("Enter date (YYYY-MM-DD): ")
    description = input("Enter description: ")
    
    spend_controller.add_expense(amount, category, date, description)
    print("Expense added successfully!")

def list_expenses_view():
    expenses = spend_controller.list_expenses()
    if not expenses:
        print("No expenses found.")
        return
    
    for expense in expenses:
        print(f"Amount: {expense.amount}, Category: {expense.category}, Date: {expense.date}, Description: {expense.description}")

def filter_expenses_view():
    category = input("Enter category to filter: ")
    filtered_expenses = spend_controller.filter_expenses(category)
    
    if not filtered_expenses:
        print("No expenses found for this category.")
        return
    
    for expense in filtered_expenses:
        print(f"Amount: {expense.amount}, Category: {expense.category}, Date: {expense.date}, Description: {expense.description}")
