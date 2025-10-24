# 🚀 Quick Start Guide - SpendSense

Get SpendSense up and running in 5 minutes!

## Prerequisites
- Python 3.8+ installed
- pip package manager
- Web browser (Chrome, Firefox, Safari, or Edge)

## Installation Steps

### 1. Clone & Navigate
```bash
git clone https://github.com/ropa1295/SpendSense.git
cd SpendSense
```

### 2. Set Up Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch Application
```bash
python src/main.py
```

### 5. Open Browser
Navigate to: **http://localhost:5000**

## 🎉 You're Ready!

The application will initialize with sample data to help you explore features.

## First Steps

1. **Explore Dashboard**: View the financial health meter and recent transactions
2. **Add Transaction**: Click "+ New Expense" to record your first transaction
3. **Set Budget**: Navigate to the top bar and set a monthly budget
4. **Create Goal**: Go to Goals tab and set your first savings goal
5. **View Analytics**: Check the History tab for spending trends

## Need Help?

- Full documentation: See [README.md](README.md)
- API docs: Visit http://localhost:5000/api/docs/
- Issues: Report on GitHub

## Quick Commands

```bash
# Start application
python src/main.py

# Start without sample data
# (Edit src/main.py and comment out initialize_sample_data())
python src/main.py

# Run on different port
# (Edit src/main.py, change port=5000 to desired port)
python src/main.py

# Deactivate virtual environment
deactivate
```

## Troubleshooting

**Port already in use?**
- Change the port in `src/main.py` or `src/web_app.py`

**Module not found?**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

**Charts not showing?**
- Check that matplotlib is properly installed
- Try: `pip install --upgrade matplotlib`

---

Happy budgeting! 💰✨
