from web_app import app, spend_controller
from datetime import datetime, timedelta
import random

def initialize_sample_data():
    """Initialize the app with 15 expenses for October ($1000) and 25 expenses per month for the previous 5 months (max $1700 per month)"""
    
    # Check if expenses already exist
    existing_expenses = spend_controller.get_all_expenses()
    if len(existing_expenses) > 0:
        print("📊 Sample data already exists. Skipping initialization.")
        return
    
    print("📝 Initializing with sample expenses for October and the past 5 months...")
    
    # Expanded categories for more realistic data
    categories = [
        'Groceries', 'Dining Out', 'Coffee/Snacks', 'Fuel/Gas', 
        'Shopping/Clothing', 'Entertainment', 'Utilities', 
        'Public Transit', 'Health Insurance', 'Subscriptions',
        'Rent/Mortgage', 'Internet', 'Gym/Fitness', 'Beauty/Personal Care',
        'Home Supplies', 'Phone Bill', 'Streaming Services', 'Books/Education',
        'Pet Care', 'Gifts', 'Car Maintenance', 'Parking', 'Medical/Pharmacy'
    ]
    
    # Descriptions for each category
    descriptions = {
        'Groceries': ['Weekly grocery shopping', 'Fresh produce', 'Supermarket run', 'Pantry essentials', 'Organic food'],
        'Dining Out': ['Dinner at restaurant', 'Lunch with friends', 'Weekend brunch', 'Thai takeout', 'Pizza night'],
        'Coffee/Snacks': ['Morning coffee', 'Afternoon snack', 'Coffee shop visit', 'Bakery treats', 'Bubble tea'],
        'Fuel/Gas': ['Gas station fill-up', 'Fuel refill', 'Weekly gas', 'Car fuel', 'Road trip gas'],
        'Shopping/Clothing': ['New shoes', 'Clothing purchase', 'Online shopping', 'Weekend shopping', 'Sale items'],
        'Entertainment': ['Movie tickets', 'Concert tickets', 'Streaming service', 'Game purchase', 'Theater show'],
        'Utilities': ['Electricity bill', 'Water bill', 'Gas bill', 'Trash service', 'Utilities'],
        'Public Transit': ['Bus pass', 'Metro card', 'Train ticket', 'Transit pass', 'Uber ride'],
        'Health Insurance': ['Health premium', 'Insurance payment', 'Medical coverage', 'Health plan', 'Dental insurance'],
        'Subscriptions': ['Netflix subscription', 'Spotify premium', 'Cloud storage', 'App subscription', 'Magazine'],
        'Rent/Mortgage': ['Monthly rent', 'Mortgage payment', 'Rent', 'Housing payment'],
        'Internet': ['Internet bill', 'WiFi service', 'Broadband', 'ISP payment'],
        'Gym/Fitness': ['Gym membership', 'Yoga class', 'Fitness class', 'Personal trainer', 'Sports equipment'],
        'Beauty/Personal Care': ['Haircut', 'Salon visit', 'Spa treatment', 'Skincare', 'Cosmetics'],
        'Home Supplies': ['Cleaning supplies', 'Home decor', 'Kitchen items', 'Furniture', 'Household goods'],
        'Phone Bill': ['Mobile bill', 'Phone service', 'Cell phone', 'Data plan'],
        'Streaming Services': ['Hulu', 'Disney+', 'Prime Video', 'HBO Max', 'YouTube Premium'],
        'Books/Education': ['Online course', 'Textbook', 'E-book', 'Audiobook', 'Educational material'],
        'Pet Care': ['Pet food', 'Vet visit', 'Pet supplies', 'Grooming', 'Pet medication'],
        'Gifts': ['Birthday gift', 'Anniversary present', 'Holiday gift', 'Thank you gift', 'Gift card'],
        'Car Maintenance': ['Oil change', 'Car wash', 'Tire rotation', 'Car repair', 'Auto service'],
        'Parking': ['Parking fee', 'Garage parking', 'Street parking', 'Parking meter', 'Monthly parking'],
        'Medical/Pharmacy': ['Prescription', 'Doctor visit', 'Pharmacy', 'Medicine', 'Medical supplies']
    }
    
    total_created = 0
    today = datetime.now()
    
    # First, generate 15 expenses for October 2025 totaling $1000
    print("   Creating October expenses...")
    october_total = 1000.0
    october_amounts = []
    remaining = october_total
    
    for i in range(14):
        min_amount = 10.0
        max_amount = min(remaining * 0.15, remaining - (14 - i) * min_amount)
        if max_amount < min_amount:
            max_amount = min_amount
        
        amount = round(random.uniform(min_amount, max_amount), 2)
        october_amounts.append(amount)
        remaining -= amount
    
    # Last amount is whatever's remaining
    october_amounts.append(round(remaining, 2))
    random.shuffle(october_amounts)
    
    # Create October expenses
    october_start = datetime(today.year, today.month, 1)
    days_in_october = today.day  # Only up to today
    
    for amount in october_amounts:
        day_offset = random.randint(0, days_in_october - 1)
        expense_date = (october_start + timedelta(days=day_offset)).strftime('%Y-%m-%d')
        
        category = random.choice(categories)
        description = random.choice(descriptions[category]) if category in descriptions else f"{category} purchase"
        
        spend_controller.add_expense(
            amount=amount,
            category=category,
            date=expense_date,
            description=description
        )
        total_created += 1
    
    print(f"   ✓ October 2025: 15 expenses totaling ${sum(october_amounts):.2f}")
    
    # Now generate expenses for the previous 5 months (September back to May)
    for month_offset in range(1, 6):
        # Calculate target month
        target_date = today - timedelta(days=30 * month_offset)
        year = target_date.year
        month = target_date.month
        
        # Get first and last day of month
        month_start = datetime(year, month, 1)
        if month == 12:
            month_end = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            month_end = datetime(year, month + 1, 1) - timedelta(days=1)
        
        # Random total for this month (between $1400 and $1700)
        month_total = round(random.uniform(1400, 1700), 2)
        
        # Generate 25 expenses for this month
        amounts = []
        remaining = month_total
        
        for i in range(24):
            # Each expense gets a random portion
            min_amount = 5.0
            max_amount = min(remaining * 0.15, remaining - (24 - i) * min_amount)
            if max_amount < min_amount:
                max_amount = min_amount
            
            amount = round(random.uniform(min_amount, max_amount), 2)
            amounts.append(amount)
            remaining -= amount
        
        # Last amount is whatever's remaining
        amounts.append(round(remaining, 2))
        
        # Shuffle amounts for variety
        random.shuffle(amounts)
        
        # Create expenses
        days_in_month = (month_end - month_start).days + 1
        
        for i, amount in enumerate(amounts):
            # Random date within the month
            day_offset = random.randint(0, days_in_month - 1)
            expense_date = (month_start + timedelta(days=day_offset)).strftime('%Y-%m-%d')
            
            # Random category
            category = random.choice(categories)
            
            # Random description for category
            if category in descriptions:
                description = random.choice(descriptions[category])
            else:
                description = f"{category} purchase"
            
            # Create expense
            spend_controller.add_expense(
                amount=amount,
                category=category,
                date=expense_date,
                description=description
            )
            total_created += 1
        
        print(f"   ✓ {month_start.strftime('%B %Y')}: 25 expenses totaling ${sum(amounts):.2f}")
    
    print(f"✅ Created {total_created} sample expenses across 6 months")
    print(f"   October 2025: $1,000 (15 expenses)")
    print(f"   Previous 5 months: ~$1,550 average (25 expenses each)")

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 Starting Spending Sense Application")
    print("=" * 70)
    
    # Initialize sample data
    initialize_sample_data()
    
    print(f"\n📱 Web Interface:")
    print(f"   http://localhost:5000")
    print(f"\n📚 API Documentation (Swagger UI):")
    print(f"   http://localhost:5000/api/docs/")
    print(f"\n🔧 API Endpoints:")
    print(f"   GET    /api/expenses - List all expenses")
    print(f"   POST   /api/expenses - Create new expense")
    print(f"   GET    /api/expenses/<id> - Get specific expense")
    print(f"   PUT    /api/expenses/<id> - Update expense")
    print(f"   DELETE /api/expenses/<id> - Delete expense")
    print(f"   GET    /api/expenses/export/csv - Export to CSV")
    print(f"\n📊 Additional Endpoints:")
    print(f"   GET    /api/stats - Get statistics")
    print(f"   GET    /api/chart/category - Get category chart")
    print(f"\n✨ Features:")
    print(f"   ✓ Beautiful web interface")
    print(f"   ✓ Interactive API documentation")
    print(f"   ✓ Full CRUD operations")
    print(f"   ✓ Filter by category")
    print(f"   ✓ Statistics and charts")
    print(f"   ✓ CSV export")
    print("\n" + "=" * 70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)