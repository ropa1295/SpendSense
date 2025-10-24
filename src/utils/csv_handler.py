import csv
from typing import List, Dict

def export_expenses_to_csv(expenses: List[Dict], file_path: str) -> None:
    if not expenses:
        raise ValueError("No expenses to export.")
    
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=expenses[0].keys())
        writer.writeheader()
        writer.writerows(expenses)