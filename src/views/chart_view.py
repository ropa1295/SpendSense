from matplotlib import pyplot as plt

def generate_expense_chart(expenses):
    categories = {}
    
    for expense in expenses:
        category = expense.category
        amount = expense.amount
        if category in categories:
            categories[category] += amount
        else:
            categories[category] = amount

    plt.figure(figsize=(10, 6))
    plt.bar(categories.keys(), categories.values(), color='skyblue')
    plt.title('Expenses by Category')
    plt.xlabel('Category')
    plt.ylabel('Total Amount')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()