from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from controllers.spend_controller import SpendController
from controllers.sense_controller import SenseController
from datetime import datetime
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)

# Configure Flask-RESTX
api = Api(
    app,
    version='1.0',
    title='Expense Tracker API',
    description='A simple expense tracking API with CRUD operations, filtering, CSV export, and budget management',
    doc='/api/docs/',
    prefix='/api'
)

# Create namespaces
ns_expenses = api.namespace('expenses', description='Expense operations')
ns_budgets = api.namespace('budgets', description='Budget operations')

spend_controller = SpendController()
sense_controller = SenseController()

# Define models for API documentation
expense_model = api.model('Expense', {
    'id': fields.String(readonly=True, description='Unique expense identifier'),
    'amount': fields.Float(required=True, description='Expense amount', example=25.50),
    'category': fields.String(required=True, description='Expense category', example='Food'),
    'date': fields.String(description='Expense date (YYYY-MM-DD)', example='2024-10-24'),
    'description': fields.String(required=True, description='Expense description', example='Lunch'),
    'created_at': fields.String(readonly=True, description='Creation timestamp')
})

budget_model = api.model('Budget', {
    'id': fields.String(readonly=True, description='Unique budget identifier'),
    'amount': fields.Float(required=True, description='Budget amount', example=1000.00),
    'month': fields.String(required=True, description='Month (YYYY-MM)', example='2024-10'),
    'category': fields.String(description='Category (null for total budget)', example='Food'),
    'created_at': fields.String(readonly=True, description='Creation timestamp')
})

budget_input_model = api.model('BudgetInput', {
    'amount': fields.Float(required=True, description='Budget amount', example=1000.00),
    'month': fields.String(required=True, description='Month (YYYY-MM)', example='2024-10'),
    'category': fields.String(description='Category (leave empty for total budget)', example='Food')
})

expense_input_model = api.model('ExpenseInput', {
    'amount': fields.Float(required=True, description='Expense amount', example=25.50),
    'category': fields.String(required=True, description='Expense category', example='Food'),
    'date': fields.String(description='Expense date (YYYY-MM-DD)', example='2024-10-24'),
    'description': fields.String(required=True, description='Expense description', example='Lunch')
})

expense_list_model = api.model('ExpenseList', {
    'expenses': fields.List(fields.Nested(expense_model)),
    'count': fields.Integer(description='Total number of expenses')
})

response_model = api.model('Response', {
    'success': fields.Boolean(description='Success status'),
    'expense': fields.Nested(expense_model, description='Expense data'),
    'message': fields.String(description='Response message')
})

# Web Interface Route (not in API namespace)
@app.route('/')
def index():
    """Render the main web interface"""
    return render_template('index.html')

# API Routes with documentation
@ns_expenses.route('')
class ExpenseListResource(Resource):
    @ns_expenses.doc('list_expenses', params={
        'category': 'Filter by category',
        'tag': 'Filter by tag'
    })
    @ns_expenses.marshal_with(expense_list_model)
    def get(self):
        """List all expenses with optional filtering"""
        category = request.args.get('category')
        tag = request.args.get('tag')
        
        if category or tag:
            expenses = spend_controller.filter_expenses(category=category, tag=tag)
        else:
            expenses = spend_controller.get_all_expenses()
        
        return {
            'expenses': [expense.to_dict() for expense in expenses],
            'count': len(expenses)
        }
    
    @ns_expenses.doc('create_expense')
    @ns_expenses.expect(expense_input_model, validate=True)
    @ns_expenses.marshal_with(response_model, code=201)
    @ns_expenses.response(400, 'Validation error')
    def post(self):
        """Create a new expense"""
        data = api.payload
        
        try:
            amount = float(data['amount'])
            category = data['category']
            date = data.get('date', datetime.now().strftime("%Y-%m-%d"))
            description = data.get('description', '')
            
            expense = spend_controller.add_expense(amount, category, date, description)
            
            # Return response in expected format for web UI
            response = {
                'success': True,
                'expense': expense.to_dict(),
                'message': 'Expense created successfully'
            }
            return response, 201
        except KeyError as e:
            api.abort(400, f'Missing required field: {str(e)}')
        except ValueError as e:
            api.abort(400, f'Invalid value: {str(e)}')
        except Exception as e:
            api.abort(500, f'Error creating expense: {str(e)}')

@ns_expenses.route('/<string:expense_id>')
@ns_expenses.param('expense_id', 'The expense identifier')
class ExpenseResource(Resource):
    @ns_expenses.doc('get_expense')
    @ns_expenses.response(200, 'Success', expense_model)
    @ns_expenses.response(404, 'Expense not found')
    def get(self, expense_id):
        """Get a specific expense by ID"""
        expense = spend_controller.get_expense_by_id(expense_id)
        if expense:
            return {'expense': expense.to_dict()}
        api.abort(404, f'Expense {expense_id} not found')
    
    @ns_expenses.doc('update_expense')
    @ns_expenses.expect(expense_input_model)
    @ns_expenses.marshal_with(response_model)
    @ns_expenses.response(404, 'Expense not found')
    def put(self, expense_id):
        """Update an existing expense"""
        data = api.payload
        
        try:
            amount = float(data.get('amount')) if data.get('amount') else None
            category = data.get('category')
            date = data.get('date')
            description = data.get('description')
            
            updated_expense = spend_controller.update_expense(
                expense_id, amount, category, date, description
            )
            
            if updated_expense:
                return {
                    'success': True,
                    'expense': updated_expense.to_dict(),
                    'message': 'Expense updated successfully'
                }
            api.abort(404, f'Expense {expense_id} not found')
        except ValueError as e:
            api.abort(400, f'Invalid value: {str(e)}')
        except Exception as e:
            api.abort(500, f'Error updating expense: {str(e)}')
    
    @ns_expenses.doc('delete_expense')
    @ns_expenses.response(200, 'Success')
    @ns_expenses.response(404, 'Expense not found')
    def delete(self, expense_id):
        """Delete an expense"""
        if spend_controller.delete_expense(expense_id):
            return {'success': True, 'message': 'Expense deleted successfully'}
        api.abort(404, f'Expense {expense_id} not found')

@ns_expenses.route('/export/csv')
class ExportCSVResource(Resource):
    @ns_expenses.doc('export_csv')
    @ns_expenses.response(200, 'CSV file')
    def get(self):
        """Export all expenses to CSV format"""
        csv_data = spend_controller.export_to_csv()
        
        output = io.BytesIO()
        output.write(csv_data.encode('utf-8'))
        output.seek(0)
        
        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'expenses_{datetime.now().strftime("%Y%m%d")}.csv'
        )

# Budget Routes
@ns_budgets.route('')
class BudgetListResource(Resource):
    @ns_budgets.doc('list_budgets')
    def get(self):
        """List all budgets"""
        budgets = sense_controller.get_all_budgets()
        return {
            'budgets': [b.to_dict() for b in budgets],
            'count': len(budgets)
        }
    
    @ns_budgets.doc('set_budget')
    @ns_budgets.expect(budget_input_model)
    def post(self):
        """Set or update a budget"""
        data = api.payload
        
        try:
            amount = float(data['amount'])
            month = data['month']
            category = data.get('category') or None
            
            budget = sense_controller.set_budget(amount, month, category)
            
            return {
                'success': True,
                'budget': budget.to_dict(),
                'message': 'Budget set successfully'
            }, 201
        except Exception as e:
            api.abort(400, f'Error setting budget: {str(e)}')

@ns_budgets.route('/<string:budget_id>')
class BudgetResource(Resource):
    @ns_budgets.doc('delete_budget')
    def delete(self, budget_id):
        """Delete a budget"""
        if sense_controller.delete_budget(budget_id):
            return {'success': True, 'message': 'Budget deleted successfully'}
        api.abort(404, f'Budget {budget_id} not found')

@ns_budgets.route('/analysis/<string:month>')
class BudgetAnalysisResource(Resource):
    @ns_budgets.doc('budget_analysis', params={'month': 'Month in YYYY-MM format'})
    def get(self, month):
        """Get budget vs spending analysis for a month"""
        expenses = spend_controller.get_all_expenses()
        analysis = sense_controller.calculate_spending_vs_budget(expenses, month)
        return analysis

# Additional routes for web interface (outside API namespace)
@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get expense statistics"""
    expenses = spend_controller.get_all_expenses()
    
    if not expenses:
        return jsonify({
            'total': 0,
            'count': 0,
            'by_category': {},
            'by_date': {}
        })
    
    total = sum(e.amount for e in expenses)
    
    by_category = defaultdict(float)
    for expense in expenses:
        by_category[expense.category] += expense.amount
    
    by_date = defaultdict(float)
    for expense in expenses:
        by_date[expense.date] += expense.amount
    
    return jsonify({
        'total': total,
        'count': len(expenses),
        'by_category': dict(by_category),
        'by_date': dict(sorted(by_date.items()))
    })

@app.route('/api/chart/category', methods=['GET'])
def chart_by_category():
    """Generate category pie chart"""
    # Get month and year parameters from query string
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)
    
    expenses = spend_controller.get_all_expenses()
    
    # Filter by month and year if provided
    if month is not None and year is not None:
        filtered_expenses = []
        for expense in expenses:
            expense_date = datetime.strptime(expense.date, '%Y-%m-%d')
            if expense_date.month == month and expense_date.year == year:
                filtered_expenses.append(expense)
        expenses = filtered_expenses
    
    if not expenses:
        # Return empty chart
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=14)
        ax.axis('off')
    else:
        by_category = defaultdict(float)
        for expense in expenses:
            by_category[expense.category] += expense.amount
        
        fig, ax = plt.subplots(figsize=(6, 5))
        categories = list(by_category.keys())
        amounts = list(by_category.values())
        
        colors = plt.cm.Set3(range(len(categories)))
        ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90, colors=colors)
        
        # Update title to show month/year if filtered
        if month is not None and year is not None:
            month_name = datetime(year, month, 1).strftime('%B %Y')
            ax.set_title(f'Expenses by Category - {month_name}', fontsize=14, fontweight='bold')
        else:
            ax.set_title('Expenses by Category', fontsize=14, fontweight='bold')
    
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png', bbox_inches='tight', dpi=100)
    img_bytes.seek(0)
    plt.close()
    
    return send_file(img_bytes, mimetype='image/png')

@app.route('/api/budgets/current', methods=['GET'])
def get_current_budget():
    """Get budget for current month"""
    current_month = datetime.now().strftime('%Y-%m')
    budgets = sense_controller.get_budgets_by_month(current_month)
    expenses = spend_controller.get_all_expenses()
    analysis = sense_controller.calculate_spending_vs_budget(expenses, current_month)
    
    return jsonify({
        'budgets': [b.to_dict() for b in budgets],
        'analysis': analysis
    })

@app.route('/api/chart/budget/<string:month>', methods=['GET'])
def chart_budget(month):
    """Generate budget vs spending chart"""
    expenses = spend_controller.get_all_expenses()
    analysis = sense_controller.calculate_spending_vs_budget(expenses, month)
    
    if analysis['total_budget'] == 0:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'No budget set for this month', ha='center', va='center', fontsize=16)
        ax.axis('off')
    else:
        # Create budget comparison chart
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Overall budget gauge
        total_spent = analysis['total_spent']
        total_budget = analysis['total_budget']
        remaining = analysis['total_remaining']
        
        colors_gauge = ['#48bb78' if remaining >= 0 else '#f56565', '#e2e8f0']
        sizes_gauge = [min(total_spent, total_budget), max(0, remaining)]
        
        if sum(sizes_gauge) > 0:
            ax1.pie(sizes_gauge, labels=['Spent', 'Remaining'], autopct='%1.1f%%', 
                   startangle=90, colors=colors_gauge)
        ax1.set_title(f'Overall Budget\n${total_spent:.2f} / ${total_budget:.2f}', 
                     fontsize=14, fontweight='bold')
        
        # Category comparison
        if analysis['categories']:
            categories = list(analysis['categories'].keys())
            budgets = [analysis['categories'][c]['budget'] for c in categories]
            spent = [analysis['categories'][c]['spent'] for c in categories]
            
            x = range(len(categories))
            width = 0.35
            
            ax2.bar([i - width/2 for i in x], budgets, width, label='Budget', color='#4299e1')
            ax2.bar([i + width/2 for i in x], spent, width, label='Spent', color='#ed8936')
            
            ax2.set_xlabel('Categories')
            ax2.set_ylabel('Amount ($)')
            ax2.set_title('Budget vs Spending by Category', fontsize=14, fontweight='bold')
            ax2.set_xticks(x)
            ax2.set_xticklabels(categories, rotation=45, ha='right')
            ax2.legend()
            ax2.grid(axis='y', alpha=0.3)
        else:
            ax2.text(0.5, 0.5, 'No category budgets set', ha='center', va='center', fontsize=14)
            ax2.axis('off')
    
    plt.tight_layout()
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png', bbox_inches='tight', dpi=100)
    img_bytes.seek(0)
    plt.close()
    
    return send_file(img_bytes, mimetype='image/png')

@app.route('/api/chart/monthly-trend', methods=['GET'])
def chart_monthly_trend():
    """Generate monthly spending trend chart"""
    expenses = spend_controller.get_all_expenses()
    
    if not expenses:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, 'No expenses to display', ha='center', va='center', fontsize=16)
        ax.axis('off')
    else:
        # Group expenses by month
        monthly_data = defaultdict(lambda: {'spent': 0, 'budget': 0})
        
        for expense in expenses:
            month = expense.date[:7]  # YYYY-MM
            monthly_data[month]['spent'] += expense.amount
        
        # Add budget data
        for budget in sense_controller.get_all_budgets():
            if not budget.category:  # Only total budgets
                monthly_data[budget.month]['budget'] = budget.amount
        
        # Sort by month
        months = sorted(monthly_data.keys())
        spent_values = [monthly_data[m]['spent'] for m in months]
        budget_values = [monthly_data[m]['budget'] for m in months]
        
        # Create line chart
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(months, spent_values, marker='o', label='Spending', linewidth=2, color='#ed8936')
        ax.plot(months, budget_values, marker='s', label='Budget', linewidth=2, 
               linestyle='--', color='#4299e1')
        
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Amount ($)', fontsize=12)
        ax.set_title('Monthly Spending Trend', fontsize=16, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        
        # Highlight over-budget months
        for i, month in enumerate(months):
            if budget_values[i] > 0 and spent_values[i] > budget_values[i]:
                ax.axvspan(i-0.3, i+0.3, alpha=0.2, color='red')
        
        plt.tight_layout()
    
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png', bbox_inches='tight', dpi=100)
    img_bytes.seek(0)
    plt.close()
    
    return send_file(img_bytes, mimetype='image/png')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Not found', 'success': False}), 404
    return render_template('index.html')

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'success': False}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)