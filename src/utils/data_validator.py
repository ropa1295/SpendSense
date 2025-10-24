def validate_amount(amount):
    if not isinstance(amount, (int, float)) or amount <= 0:
        raise ValueError("Amount must be a positive number.")

def validate_category(category):
    if not isinstance(category, str) or not category.strip():
        raise ValueError("Category must be a non-empty string.")

def validate_date(date):
    if not isinstance(date, str):
        raise ValueError("Date must be a string.")
    # Additional date format validation can be added here

def validate_description(description):
    if not isinstance(description, str):
        raise ValueError("Description must be a string.")

def validate_tags(tags):
    if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
        raise ValueError("Tags must be a list of strings.")