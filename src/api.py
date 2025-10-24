from flask import Flask, request
from flask_restx import Api, Resource, fields, reqparse
from controllers.spend_controller import SpendController
from datetime import datetime
import traceback

app = Flask(__name__)

# Configure Flask-RESTX
api = Api(
    app,
    version='1.0',
    title='Expense Tracker API',
    description='A simple expense tracking API with CRUD operations, filtering, and CSV export',
    doc='/docs/',  # Swagger UI will be available at /docs/
    prefix='/api'
)

# Create namespaces
ns_expenses = api.namespace('expenses', description='Expense operations')
ns_health = api.namespace('health', description='Health check operations')

spend_controller = SpendController()

# Define models for request/response validation and documentation
expense_model = api.model('Expense', {
    'id': fields.String(readonly=True, description='Unique expense identifier'),
    'amount': fields.Float(required=True, description='Expense amount', example=25.50),
    'category': fields.String(required=True, description='Expense category', example='Food'),
    'date': fields.String(description='Expense date (YYYY-MM-DD)', example='2024-10-24'),
    'description': fields.String(description='Expense description (optional)', example='Lunch at restaurant'),
    'created_at': fields.String(readonly=True, description='Creation timestamp')
})

expense_input_model = api.model('ExpenseInput', {
    'amount': fields.Float(required=True, description='Expense amount', example=25.50),
    'category': fields.String(required=True, description='Expense category', example='Food'),
    'date': fields.String(description='Expense date (YYYY-MM-DD), defaults to today', example='2024-10-24'),
    'description': fields.String(description='Expense description (optional)', example='Lunch at restaurant'),
})

expense_update_model = api.model('ExpenseUpdate', {
    'amount': fields.Float(description='Expense amount', example=30.00),
    'category': fields.String(description='Expense category', example='Dining'),
    'date': fields.String(description='Expense date (YYYY-MM-DD)', example='2024-10-24'),
    'description': fields.String(description='Expense description', example='Updated lunch'),
})

expense_list_model = api.model('ExpenseList', {
    'expenses': fields.List(fields.Nested(expense_model)),
    'count': fields.Integer(description='Total number of expenses')
})

message_model = api.model('Message', {
    'message': fields.String(description='Response message')
})

error_model = api.model('Error', {
    'error': fields.String(description='Error message')
})

health_model = api.model('Health', {
    'status': fields.String(description='Health status'),
    'message': fields.String(description='Health message')
})

csv_export_model = api.model('CSVExport', {
    'message': fields.String(description='Export message'),
    'data': fields.String(description='CSV data as string')
})

# Create parsers for query parameters
expense_parser = reqparse.RequestParser()
expense_parser.add_argument('category', type=str, help='Filter by category')
expense_parser.add_argument('date_from', type=str, help='Filter from date (YYYY-MM-DD)')
expense_parser.add_argument('date_to', type=str, help='Filter to date (YYYY-MM-DD)')
expense_parser.add_argument('tag', type=str, help='Filter by tag')

@ns_health.route('')
class HealthCheck(Resource):
    @ns_health.doc('health_check')
    @ns_health.marshal_with(health_model)
    def get(self):
        """Health check endpoint"""
        return {
            'status': 'healthy',
            'message': 'Expense Tracker API is running'
        }

@ns_expenses.route('')
class ExpenseList(Resource):
    @ns_expenses.doc('list_expenses')
    @ns_expenses.expect(expense_parser)
    @ns_expenses.marshal_with(expense_list_model)
    def get(self):
        """Get all expenses with optional filtering"""
        args = expense_parser.parse_args()
        category = args['category']
        date_from = args['date_from']
        date_to = args['date_to']
        tag = args['tag']
        
        try:
            if any([category, date_from, date_to, tag]):
                expenses = spend_controller.filter_expenses(category, date_from, date_to, tag)
            else:
                expenses = spend_controller.get_all_expenses()
            
            return {
                'expenses': [expense.to_dict() for expense in expenses],
                'count': len(expenses)
            }
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')

    @ns_expenses.doc('create_expense')
    @ns_expenses.expect(expense_input_model)
    @ns_expenses.marshal_with(expense_model, code=201)
    def post(self):
        """Create a new expense"""
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['amount', 'category', 'description']
            for field in required_fields:
                if field not in data:
                    api.abort(400, f'Missing required field: {field}')
            
            # Set default values
            amount = float(data['amount'])
            category = data['category']
            date = data.get('date', datetime.now().strftime("%Y-%m-%d"))
            description = data['description']
            
            expense = spend_controller.add_expense(amount, category, date, description)
            
            return expense.to_dict(), 201
        except ValueError as e:
            api.abort(400, 'Invalid amount value')
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')

@ns_expenses.route('/<string:expense_id>')
@ns_expenses.param('expense_id', 'The expense identifier')
class Expense(Resource):
    @ns_expenses.doc('get_expense')
    @ns_expenses.marshal_with(expense_model)
    def get(self, expense_id):
        """Get a specific expense by ID"""
        try:
            expense = spend_controller.get_expense_by_id(expense_id)
            if expense:
                return expense.to_dict()
            else:
                api.abort(404, 'Expense not found')
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')

    @ns_expenses.doc('update_expense')
    @ns_expenses.expect(expense_update_model)
    @ns_expenses.marshal_with(expense_model)
    def put(self, expense_id):
        """Update an existing expense"""
        try:
            data = request.get_json()
            
            # Extract update fields
            amount = float(data['amount']) if 'amount' in data else None
            category = data.get('category')
            date = data.get('date')
            description = data.get('description')
            
            updated_expense = spend_controller.update_expense(
                expense_id, amount, category, date, description
            )
            
            if updated_expense:
                return updated_expense.to_dict()
            else:
                api.abort(404, 'Expense not found')
        except ValueError as e:
            api.abort(400, 'Invalid amount value')
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')

    @ns_expenses.doc('delete_expense')
    @ns_expenses.marshal_with(message_model)
    def delete(self, expense_id):
        """Delete an expense"""
        try:
            if spend_controller.delete_expense(expense_id):
                return {'message': 'Expense deleted successfully'}
            else:
                api.abort(404, 'Expense not found')
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')

@ns_expenses.route('/export/csv')
class ExpenseCSVExport(Resource):
    @ns_expenses.doc('export_csv')
    @ns_expenses.marshal_with(csv_export_model)
    def get(self):
        """Export all expenses to CSV format"""
        try:
            csv_data = spend_controller.export_to_csv()
            return {
                'message': 'CSV export completed',
                'data': csv_data
            }
        except Exception as e:
            api.abort(500, f'Internal server error: {str(e)}')

# Global error handlers
@api.errorhandler
def default_error_handler(error):
    """Default error handler"""
    return {'error': str(error)}, getattr(error, 'code', 500)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)