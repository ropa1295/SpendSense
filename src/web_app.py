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

# Initialize Flask-RESTX API
api = Api(
    app,
    version='2.0',
    title='SpendSense Financial Management API',
    description='Smart personal finance tracking with transaction management, budget planning, analytics, and data export capabilities',
    doc='/api/docs/',
    prefix='/api'
)

# Initialize controllers
spend_controller = SpendController()
sense_controller = SenseController()

# Create API namespaces
ns_expenses = api.namespace('expenses', description='Transaction and spending management')
ns_budgets = api.namespace('budgets', description='Financial planning and budget control')

# API Documentation Models
expense_model = api.model('Transaction', {
    'id': fields.String(readonly=True, description='Transaction unique identifier'),
    'amount': fields.Float(required=True, description='Transaction amount', example=25.50),
    'category': fields.String(required=True, description='Spending category', example='Food'),
    'date': fields.String(description='Transaction date (YYYY-MM-DD)', example='2024-10-24'),
    'description': fields.String(required=True, description='Transaction notes', example='Lunch'),
    'created_at': fields.String(readonly=True, description='Record creation timestamp')
})

expense_input_model = api.model('TransactionInput', {
    'amount': fields.Float(required=True, description='Transaction amount', example=25.50),
    'category': fields.String(required=True, description='Spending category', example='Food'),
    'date': fields.String(description='Transaction date (YYYY-MM-DD)', example='2024-10-24'),
    'description': fields.String(required=True, description='Transaction notes', example='Lunch')
})

expense_list_model = api.model('TransactionList', {
    'expenses': fields.List(fields.Nested(expense_model)),
    'count': fields.Integer(description='Total transaction count')
})

response_model = api.model('ApiResponse', {
    'success': fields.Boolean(description='Operation success indicator'),
    'expense': fields.Nested(expense_model, description='Transaction data'),
    'message': fields.String(description='Status message')
})

budget_model = api.model('BudgetPlan', {
    'id': fields.String(readonly=True, description='Budget plan identifier'),
    'amount': fields.Float(required=True, description='Allocated budget amount', example=1000.00),
    'month': fields.String(required=True, description='Budget period (YYYY-MM)', example='2024-10'),
    'category': fields.String(description='Spending category (optional for overall budget)', example='Food'),
    'created_at': fields.String(readonly=True, description='Plan creation timestamp')
})

budget_input_model = api.model('BudgetPlanInput', {
    'amount': fields.Float(required=True, description='Budget allocation amount', example=1000.00),
    'month': fields.String(required=True, description='Budget period (YYYY-MM)', example='2024-10'),
    'category': fields.String(description='Spending category (optional)', example='Food')
})

# Primary Web Interface
@app.route('/')
def home_dashboard():
    """Serve the main SpendSense dashboard"""
    return render_template('index.html')

# Transaction Management Endpoints
@ns_expenses.route('')
class TransactionCollection(Resource):
    @ns_expenses.doc('retrieve_all_transactions', params={
        'category': 'Category filter',
        'tag': 'Tag filter'
    })
    @ns_expenses.marshal_with(expense_list_model)
    def get(self):
        """Retrieve all transactions with optional category/tag filtering"""
        category_filter = request.args.get('category')
        tag_filter = request.args.get('tag')
        
        if category_filter or tag_filter:
            transaction_list = spend_controller.filter_expenses(category=category_filter, tag=tag_filter)
        else:
            transaction_list = spend_controller.get_all_expenses()
        
        return {
            'expenses': [txn.to_dict() for txn in transaction_list],
            'count': len(transaction_list)
        }
    
    @ns_expenses.doc('record_new_transaction')
    @ns_expenses.expect(expense_input_model, validate=True)
    @ns_expenses.marshal_with(response_model, code=201)
    @ns_expenses.response(400, 'Invalid input data')
    def post(self):
        """Record a new financial transaction"""
        payload = api.payload
        
        try:
            txn_amount = float(payload['amount'])
            txn_category = payload['category']
            txn_date = payload.get('date', datetime.now().strftime("%Y-%m-%d"))
            txn_notes = payload.get('description', '')
            
            new_expense = spend_controller.add_expense(txn_amount, txn_category, txn_date, txn_notes)
            
            # Format response for web interface compatibility
            api_response = {
                'success': True,
                'expense': new_expense.to_dict(),
                'message': 'Transaction recorded successfully'
            }
            return api_response, 201
        except KeyError as e:
            api.abort(400, f'Required field missing: {str(e)}')
        except ValueError as e:
            api.abort(400, f'Invalid data format: {str(e)}')
        except Exception as e:
            api.abort(500, f'Transaction creation failed: {str(e)}')

@ns_expenses.route('/<string:expense_id>')
@ns_expenses.param('expense_id', 'Transaction identifier')
class TransactionResource(Resource):
    @ns_expenses.doc('fetch_transaction_details')
    @ns_expenses.response(200, 'Transaction found', expense_model)
    @ns_expenses.response(404, 'Transaction not found')
    def get(self, expense_id):
        """Fetch details of a specific transaction"""
        transaction = spend_controller.get_expense_by_id(expense_id)
        if transaction:
            return {'expense': transaction.to_dict()}
        api.abort(404, f'Transaction {expense_id} does not exist')
    
    @ns_expenses.doc('modify_transaction')
    @ns_expenses.expect(expense_input_model)
    @ns_expenses.marshal_with(response_model)
    @ns_expenses.response(404, 'Transaction not found')
    def put(self, expense_id):
        """Modify an existing transaction record"""
        payload = api.payload
        
        try:
            updated_amount = float(payload.get('amount')) if payload.get('amount') else None
            updated_category = payload.get('category')
            updated_date = payload.get('date')
            updated_notes = payload.get('description')
            
            modified_expense = spend_controller.update_expense(
                expense_id, updated_amount, updated_category, updated_date, updated_notes
            )
            
            if modified_expense:
                return {
                    'success': True,
                    'expense': modified_expense.to_dict(),
                    'message': 'Transaction modified successfully'
                }
            api.abort(404, f'Transaction {expense_id} does not exist')
        except ValueError as e:
            api.abort(400, f'Invalid data format: {str(e)}')
        except Exception as e:
            api.abort(500, f'Transaction update failed: {str(e)}')
    
    @ns_expenses.doc('remove_transaction')
    @ns_expenses.response(200, 'Transaction removed')
    @ns_expenses.response(404, 'Transaction not found')
    def delete(self, expense_id):
        """Remove a transaction from records"""
        if spend_controller.delete_expense(expense_id):
            return {'success': True, 'message': 'Transaction removed successfully'}
        api.abort(404, f'Transaction {expense_id} does not exist')

@ns_expenses.route('/export/csv')
class DataExportResource(Resource):
    @ns_expenses.doc('export_transactions_csv')
    @ns_expenses.response(200, 'CSV export file generated')
    def get(self):
        """Generate CSV export of all transactions"""
        csv_content = spend_controller.export_to_csv()
        
        buffer = io.BytesIO()
        buffer.write(csv_content.encode('utf-8'))
        buffer.seek(0)
        
        timestamp = datetime.now().strftime("%Y%m%d")
        return send_file(
            buffer,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'spendsense_transactions_{timestamp}.csv'
        )

# Budget Planning Endpoints
@ns_budgets.route('')
class BudgetPlanCollection(Resource):
    @ns_budgets.doc('retrieve_all_budgets')
    def get(self):
        """Retrieve all budget plans"""
        budget_plans = sense_controller.get_all_budgets()
        return {
            'budgets': [plan.to_dict() for plan in budget_plans],
            'count': len(budget_plans)
        }
    
    @ns_budgets.doc('create_budget_plan')
    @ns_budgets.expect(budget_input_model)
    def post(self):
        """Create or update a budget plan"""
        payload = api.payload
        
        try:
            budget_amount = float(payload['amount'])
            budget_period = payload['month']
            budget_category = payload.get('category') or None
            
            new_budget = sense_controller.set_budget(budget_amount, budget_period, budget_category)
            
            return {
                'success': True,
                'budget': new_budget.to_dict(),
                'message': 'Budget plan created successfully'
            }, 201
        except Exception as e:
            api.abort(400, f'Budget creation failed: {str(e)}')

@ns_budgets.route('/analysis/<string:month>')
class BudgetAnalyticsResource(Resource):
    @ns_budgets.doc('analyze_budget_performance', params={'month': 'Period in YYYY-MM format'})
    def get(self, month):
        """Analyze budget performance vs actual spending for a period"""
        transaction_list = spend_controller.get_all_expenses()
        performance_data = sense_controller.calculate_spending_vs_budget(transaction_list, month)
        return performance_data

@ns_budgets.route('/<string:budget_id>')
class BudgetPlanResource(Resource):
    @ns_budgets.doc('remove_budget_plan')
    def delete(self, budget_id):
        """Remove a budget plan"""
        if sense_controller.delete_budget(budget_id):
            return {'success': True, 'message': 'Budget plan removed successfully'}
        api.abort(404, f'Budget plan {budget_id} does not exist')

# Supplementary Web Interface Routes
@app.route('/api/stats', methods=['GET'])
def fetch_spending_statistics():
    """Retrieve comprehensive spending statistics"""
    transaction_list = spend_controller.get_all_expenses()
    
    if not transaction_list:
        return jsonify({
            'total': 0,
            'count': 0,
            'by_category': {},
            'by_date': {}
        })
    
    total_spent = sum(txn.amount for txn in transaction_list)
    
    category_totals = defaultdict(float)
    for txn in transaction_list:
        category_totals[txn.category] += txn.amount
    
    daily_totals = defaultdict(float)
    for txn in transaction_list:
        daily_totals[txn.date] += txn.amount
    
    return jsonify({
        'total': total_spent,
        'count': len(transaction_list),
        'by_category': dict(category_totals),
        'by_date': dict(sorted(daily_totals.items()))
    })

@app.route('/api/chart/category', methods=['GET'])
def generate_category_distribution():
    """Generate spending distribution pie chart by category"""
    # Extract period filters from query parameters
    filter_month = request.args.get('month', type=int)
    filter_year = request.args.get('year', type=int)
    
    transaction_list = spend_controller.get_all_expenses()
    
    # Apply period filtering if specified
    if filter_month is not None and filter_year is not None:
        period_filtered = []
        for txn in transaction_list:
            txn_date = datetime.strptime(txn.date, '%Y-%m-%d')
            if txn_date.month == filter_month and txn_date.year == filter_year:
                period_filtered.append(txn)
        transaction_list = period_filtered
    
    if not transaction_list:
        # Generate empty state visualization
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.text(0.5, 0.5, 'No spending data to display', ha='center', va='center', fontsize=14)
        ax.axis('off')
    else:
        category_sums = defaultdict(float)
        for txn in transaction_list:
            category_sums[txn.category] += txn.amount
        
        fig, ax = plt.subplots(figsize=(6, 5))
        category_labels = list(category_sums.keys())
        spending_values = list(category_sums.values())
        
        chart_colors = plt.cm.Set3(range(len(category_labels)))
        ax.pie(spending_values, labels=category_labels, autopct='%1.1f%%', startangle=90, colors=chart_colors)
        
        # Customize title based on filter presence
        if filter_month is not None and filter_year is not None:
            period_label = datetime(filter_year, filter_month, 1).strftime('%B %Y')
            ax.set_title(f'Category Breakdown - {period_label}', fontsize=14, fontweight='bold')
        else:
            ax.set_title('Spending by Category', fontsize=14, fontweight='bold')
    
    image_buffer = io.BytesIO()
    plt.savefig(image_buffer, format='png', bbox_inches='tight', dpi=100)
    image_buffer.seek(0)
    plt.close()
    
    return send_file(image_buffer, mimetype='image/png')

@app.route('/api/budgets/current', methods=['GET'])
def fetch_active_budget_info():
    """Retrieve current month's budget information and performance"""
    active_period = datetime.now().strftime('%Y-%m')
    period_budgets = sense_controller.get_budgets_by_month(active_period)
    transaction_list = spend_controller.get_all_expenses()
    performance_analysis = sense_controller.calculate_spending_vs_budget(transaction_list, active_period)
    
    return jsonify({
        'budgets': [plan.to_dict() for plan in period_budgets],
        'analysis': performance_analysis
    })

@app.route('/api/chart/budget/<string:month>', methods=['GET'])
def visualize_budget_comparison(month):
    """Generate comprehensive budget vs actual spending visualization"""
    transaction_list = spend_controller.get_all_expenses()
    performance_data = sense_controller.calculate_spending_vs_budget(transaction_list, month)
    
    if performance_data['total_budget'] == 0:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'No budget allocation for this period', ha='center', va='center', fontsize=16)
        ax.axis('off')
    else:
        # Generate dual-panel comparison visualization
        fig, (gauge_ax, compare_ax) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Left panel: Overall budget utilization gauge
        actual_spent = performance_data['total_spent']
        allocated_budget = performance_data['total_budget']
        budget_remaining = performance_data['total_remaining']
        
        gauge_colors = ['#48bb78' if budget_remaining >= 0 else '#f56565', '#e2e8f0']
        gauge_portions = [min(actual_spent, allocated_budget), max(0, budget_remaining)]
        
        if sum(gauge_portions) > 0:
            gauge_ax.pie(gauge_portions, labels=['Utilized', 'Available'], autopct='%1.1f%%', 
                   startangle=90, colors=gauge_colors)
        gauge_ax.set_title(f'Budget Utilization\n${actual_spent:.2f} of ${allocated_budget:.2f}', 
                     fontsize=14, fontweight='bold')
        
        # Right panel: Category-level comparison
        if performance_data['categories']:
            cat_names = list(performance_data['categories'].keys())
            allocated_amounts = [performance_data['categories'][c]['budget'] for c in cat_names]
            actual_amounts = [performance_data['categories'][c]['spent'] for c in cat_names]
            
            bar_positions = range(len(cat_names))
            bar_width = 0.35
            
            compare_ax.bar([i - bar_width/2 for i in bar_positions], allocated_amounts, bar_width, 
                          label='Allocated', color='#4299e1')
            compare_ax.bar([i + bar_width/2 for i in bar_positions], actual_amounts, bar_width, 
                          label='Actual', color='#ed8936')
            
            compare_ax.set_xlabel('Spending Categories')
            compare_ax.set_ylabel('Dollar Amount ($)')
            compare_ax.set_title('Category-Level Budget Analysis', fontsize=14, fontweight='bold')
            compare_ax.set_xticks(bar_positions)
            compare_ax.set_xticklabels(cat_names, rotation=45, ha='right')
            compare_ax.legend()
            compare_ax.grid(axis='y', alpha=0.3)
        else:
            compare_ax.text(0.5, 0.5, 'No category-specific budgets', ha='center', va='center', fontsize=14)
            compare_ax.axis('off')
    
    plt.tight_layout()
    image_buffer = io.BytesIO()
    plt.savefig(image_buffer, format='png', bbox_inches='tight', dpi=100)
    image_buffer.seek(0)
    plt.close()
    
    return send_file(image_buffer, mimetype='image/png')

@app.route('/api/chart/monthly-trend', methods=['GET'])
def generate_spending_timeline():
    """Generate historical spending trend visualization"""
    transaction_list = spend_controller.get_all_expenses()
    
    if not transaction_list:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, 'Insufficient data for trend analysis', ha='center', va='center', fontsize=16)
        ax.axis('off')
    else:
        # Aggregate transactions by month
        period_aggregates = defaultdict(lambda: {'spent': 0, 'budget': 0})
        
        for txn in transaction_list:
            period_key = txn.date[:7]  # Extract YYYY-MM
            period_aggregates[period_key]['spent'] += txn.amount
        
        # Incorporate budget allocations
        for budget_plan in sense_controller.get_all_budgets():
            if not budget_plan.category:  # Overall budgets only
                period_aggregates[budget_plan.month]['budget'] = budget_plan.amount
        
        # Chronologically order periods
        sorted_periods = sorted(period_aggregates.keys())
        actual_spending = [period_aggregates[p]['spent'] for p in sorted_periods]
        planned_budgets = [period_aggregates[p]['budget'] for p in sorted_periods]
        
        # Construct timeline visualization
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.plot(sorted_periods, actual_spending, marker='o', label='Actual Spending', 
               linewidth=2, color='#ed8936')
        ax.plot(sorted_periods, planned_budgets, marker='s', label='Planned Budget', 
               linewidth=2, linestyle='--', color='#4299e1')
        
        ax.set_xlabel('Time Period', fontsize=12)
        ax.set_ylabel('Dollar Amount ($)', fontsize=12)
        ax.set_title('Spending Trend Over Time', fontsize=16, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        
        # Highlight overspending periods
        for idx, period in enumerate(sorted_periods):
            if planned_budgets[idx] > 0 and actual_spending[idx] > planned_budgets[idx]:
                ax.axvspan(idx-0.3, idx+0.3, alpha=0.2, color='red')
        
        plt.tight_layout()
    
    image_buffer = io.BytesIO()
    plt.savefig(image_buffer, format='png', bbox_inches='tight', dpi=100)
    image_buffer.seek(0)
    plt.close()
    
    return send_file(image_buffer, mimetype='image/png')

# Global Error Handlers
@app.errorhandler(404)
def handle_not_found(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Resource not found', 'success': False}), 404
    return render_template('index.html')

@app.errorhandler(500)
def handle_server_error(error):
    return jsonify({'error': 'Server encountered an error', 'success': False}), 500

# Application Entry Point
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)