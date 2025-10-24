# 💰 SpendSense

**SpendSense** is a comprehensive personal finance management application that helps you track expenses, manage budgets, set financial goals, and analyze spending patterns with beautiful visualizations.

![SpendSense Dashboard](https://img.shields.io/badge/Version-2.0-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-2.0+-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Screenshots](#-screenshots)
- [Configuration](#-configuration)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 💳 Transaction Management
- **Add, Edit, Delete Transactions**: Easily manage your financial transactions
- **Categorization**: Organize expenses into 20+ predefined categories
- **Date Filtering**: View transactions by month and year
- **CSV Export**: Download your transaction history for external analysis
- **Real-time Updates**: Instant dashboard updates when transactions change

### 📊 Budget Planning
- **Monthly Budgets**: Set overall and category-specific budgets
- **Budget Tracking**: Monitor spending vs. budget in real-time
- **Visual Alerts**: Get warnings when approaching or exceeding budgets
- **Budget Analysis**: Comprehensive budget performance metrics
- **Multi-period Comparison**: Compare budget performance across months

### 🎯 Financial Goals
- **Goal Setting**: Define savings goals with target amounts and deadlines
- **Progress Tracking**: Visual progress bars and percentage completion
- **Goal Icons**: Customize goals with emoji icons
- **Contribution Management**: Add contributions and track goal milestones
- **Achievement System**: Mark goals as complete when reached

### 📈 Analytics & Visualizations
- **Spending Breakdown**: Pie charts showing category distribution
- **Top Categories**: Bar charts highlighting biggest spending areas
- **Monthly Trends**: Line graphs tracking spending over time
- **Historical Analysis**: 6-month historical spending overview
- **Financial Health Meter**: Visual gauge of overall financial position

### 🎨 User Interface
- **Modern Design**: Clean, intuitive dashboard with card-based layout
- **Responsive**: Works seamlessly on desktop and mobile devices
- **Dark Mode Ready**: Professional color scheme with teal accents
- **Interactive Charts**: Dynamic visualizations using Matplotlib and Canvas
- **Tab Navigation**: Easy switching between Transactions, Goals, and History

---

## 🎥 Demo

### Main Dashboard
The dashboard provides an at-a-glance view of your financial health:
- Net position indicator
- Average daily spending
- Active savings goals
- Recent transactions
- Category breakdowns

### Budget Management
Set and track budgets with visual progress indicators:
- Total budget vs. actual spending
- Category-level budget tracking
- Budget utilization percentage
- Over/under budget alerts

### Goal Tracking
Create and monitor financial goals:
- Multiple concurrent goals
- Progress visualization
- Deadline tracking
- Contribution history

---

## 🛠 Tech Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask 2.0+**: Web framework
- **Flask-RESTX**: REST API with Swagger documentation
- **Flask-CORS**: Cross-origin resource sharing

### Data Visualization
- **Matplotlib**: Chart generation
- **NumPy**: Statistical calculations

### Frontend
- **HTML5/CSS3**: Modern web standards
- **JavaScript (ES6+)**: Interactive functionality
- **Canvas API**: Custom chart rendering
- **LocalStorage**: Client-side goal persistence

### Architecture
- **MVC Pattern**: Model-View-Controller separation
- **RESTful API**: Standard HTTP methods
- **Component-based**: Modular controller design

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/ropa1295/SpendSense.git
cd SpendSense
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install flask flask-restx flask-cors matplotlib numpy
```

### Step 4: Run the Application
```bash
# Initialize with sample data and start server
python src/main.py

# Or run the Flask app directly
python src/web_app.py
```

### Step 5: Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

---

## 📖 Usage

### Adding a Transaction
1. Click the **"+ New Expense"** button or **"Quick Add"** in the sidebar
2. Fill in the transaction details:
   - Amount
   - Category (select from dropdown)
   - Date
   - Description (optional)
3. Click **"Add Expense"** to save

### Setting a Budget
1. Navigate to the Transactions tab
2. Use the month selector to choose the budget period
3. Enter the budget amount
4. Select a category (leave empty for total budget)
5. Click **"Set Budget"**

### Creating a Goal
1. Switch to the **Goals** tab
2. Click **"+ Set New Goal"**
3. Enter goal details:
   - Goal name
   - Target amount
   - Current amount
   - Target date
   - Icon
4. Click **"Create Goal"**

### Viewing Analytics
1. Go to the **History** tab
2. View 6-month trends
3. Analyze spending patterns
4. Export reports for external analysis

### Exporting Data
- Click the CSV export button on any transaction view
- Downloaded file includes all transaction details
- Compatible with Excel, Google Sheets, and other tools

---

## 📁 Project Structure

```
SpendSense/
│
├── src/                          # Source code
│   ├── main.py                  # Application entry point
│   ├── web_app.py               # Flask application & routes
│   ├── api.py                   # REST API endpoints
│   │
│   ├── controllers/             # Business logic
│   │   ├── __init__.py
│   │   ├── spend_controller.py  # Transaction management
│   │   └── sense_controller.py  # Budget management
│   │
│   ├── models/                  # Data models
│   │   ├── __init__.py
│   │   ├── transaction.py       # Transaction model
│   │   └── budget_plan.py       # Budget model
│   │
│   ├── views/                   # View layer
│   │   ├── __init__.py
│   │   ├── transaction_display.py  # Transaction UI
│   │   ├── visual_analytics.py     # Chart generation
│   │   ├── expense_view.py         # Legacy wrapper
│   │   └── chart_view.py           # Legacy wrapper
│   │
│   └── utils/                   # Utility functions
│       ├── __init__.py
│       ├── csv_handler.py       # CSV export
│       └── data_validator.py    # Input validation
│
├── templates/                   # HTML templates
│   └── index.html              # Main dashboard
│
├── static/                      # Static assets
│   ├── css/
│   │   └── style.css           # Application styles
│   └── js/
│       └── app.js              # Frontend JavaScript
│
├── README.md                    # This file
├── WEB_APP.md                  # Web application architecture documentation
├── QUICKSTART.md               # Quick start guide
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
└── .gitignore                  # Git ignore file
```

---

## 🔌 API Documentation

SpendSense provides a comprehensive REST API with interactive Swagger documentation.

### API Base URL
```
http://localhost:5000/api
```

### Interactive Documentation
Access Swagger UI at:
```
http://localhost:5000/api/docs/
```

### Main Endpoints

#### Transactions
```
GET    /api/expenses              # List all transactions
POST   /api/expenses              # Create new transaction
GET    /api/expenses/{id}         # Get transaction details
PUT    /api/expenses/{id}         # Update transaction
DELETE /api/expenses/{id}         # Delete transaction
GET    /api/expenses/export/csv   # Export to CSV
```

#### Budgets
```
GET    /api/budgets               # List all budgets
POST   /api/budgets               # Create/update budget
GET    /api/budgets/analysis/{month}  # Get budget analysis
DELETE /api/budgets/{id}          # Delete budget
```

#### Analytics
```
GET    /api/stats                 # Get spending statistics
GET    /api/chart/category        # Category pie chart
GET    /api/chart/budget/{month}  # Budget comparison chart
GET    /api/chart/monthly-trend   # Monthly trend chart
```

#### Health Check
```
GET    /api/health                # Service health status
```

### Example API Calls

**Create a Transaction:**
```bash
curl -X POST http://localhost:5000/api/expenses \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 45.99,
    "category": "Groceries",
    "date": "2025-10-24",
    "description": "Weekly grocery shopping"
  }'
```

**Get Budget Analysis:**
```bash
curl http://localhost:5000/api/budgets/analysis/2025-10
```

---

## 📸 Screenshots

### Dashboard View
Main dashboard with financial health meter, spending habits, and recent transactions.

### Budget Management
Visual budget tracking with progress bars and category breakdowns.

### Goal Tracking
Interactive goal cards showing progress and achievement status.

### Historical Analysis
6-month trend charts with spending patterns and top categories.

---

## ⚙️ Configuration

### Port Configuration
Default port is 5000. To change:
```python
# In src/web_app.py or src/main.py
app.run(debug=True, host='0.0.0.0', port=YOUR_PORT)
```

### Sample Data
The application initializes with sample data for demonstration. To disable:
```python
# In src/main.py, comment out:
# initialize_sample_data()
```

### Debug Mode
For production deployment, disable debug mode:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guide for Python code
- Write descriptive commit messages
- Add comments for complex logic
- Test thoroughly before submitting
- Update documentation as needed

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Flask**: Micro web framework
- **Matplotlib**: Visualization library
- **Font Awesome**: Icons (if used)
- **Community**: Open source contributors

---

## 📞 Contact

**Project Maintainer**: ropa1295

**Repository**: [https://github.com/ropa1295/SpendSense](https://github.com/ropa1295/SpendSense)

**Issues**: [https://github.com/ropa1295/SpendSense/issues](https://github.com/ropa1295/SpendSense/issues)

---

## 🗺️ Roadmap

### Upcoming Features
- [ ] Multi-currency support
- [ ] Recurring transaction templates
- [ ] Advanced reporting and analytics
- [ ] Mobile app (React Native)
- [ ] Bank account integration
- [ ] AI-powered spending insights
- [ ] Collaborative budgets (family sharing)
- [ ] Investment tracking
- [ ] Bill reminders and notifications
- [ ] Data backup and sync

---

## 💡 Tips & Best Practices

### Getting the Most Out of SpendSense

1. **Consistent Categorization**: Use the same categories for similar expenses
2. **Regular Updates**: Record transactions daily for accurate tracking
3. **Set Realistic Budgets**: Start conservative and adjust based on actual spending
4. **Use Goals**: Break large savings targets into smaller, achievable goals
5. **Review Monthly**: Check your History tab at month-end to identify trends
6. **Export Data**: Regularly backup your data using CSV export

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: Port 5000 already in use
```bash
# Solution: Use a different port
python src/web_app.py --port 5001
```

**Issue**: Module not found errors
```bash
# Solution: Install missing dependencies
pip install flask flask-restx flask-cors matplotlib numpy
```

**Issue**: Charts not displaying
```bash
# Solution: Ensure matplotlib backend is set correctly
# In web_app.py, verify:
import matplotlib
matplotlib.use('Agg')
```

---

## 📚 Additional Resources

- **[WEB_APP.md](WEB_APP.md)**: Detailed web application architecture and implementation guide
- **[QUICKSTART.md](QUICKSTART.md)**: 5-minute quick start guide
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-RESTX Documentation](https://flask-restx.readthedocs.io/)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)
- [Personal Finance Best Practices](https://www.investopedia.com/personal-finance-4427760)

---

<div align="center">

**Made with ❤️ by the SpendSense Team**

⭐ Star us on GitHub if you find this helpful!

</div>
