from flask import Flask, request
from flask_restx import Api, Resource, fields, reqparse
from controllers.spend_controller import SpendController
from datetime import datetime
import traceback

app = Flask(__name__)

# Initialize Flask-RESTX API Gateway
api = Api(
    app,
    version='2.0',
    title='SpendSense Transaction API',
    description='Comprehensive financial transaction management system with filtering, analysis, and data export capabilities',
    doc='/docs/',  # Interactive API documentation accessible at /docs/
    prefix='/api'
)

# Initialize transaction controller
spend_controller = SpendController()

# Define API namespaces for logical grouping
ns_expenses = api.namespace('expenses', description='Financial transaction management operations')
ns_health = api.namespace('health', description='Service health monitoring')

# API Schema Models for validation and documentation
expense_model = api.model('TransactionRecord', {
    'id': fields.String(readonly=True, description='Transaction unique identifier'),
    'amount': fields.Float(required=True, description='Transaction amount', example=25.50),
    'category': fields.String(required=True, description='Spending category', example='Food'),
    'date': fields.String(description='Transaction date (YYYY-MM-DD)', example='2024-10-24'),
    'description': fields.String(description='Transaction description notes', example='Lunch at restaurant'),
    'created_at': fields.String(readonly=True, description='Record creation timestamp')
})

expense_input_model = api.model('TransactionInput', {
    'amount': fields.Float(required=True, description='Transaction amount', example=25.50),
    'category': fields.String(required=True, description='Spending category', example='Food'),
    'date': fields.String(description='Transaction date (YYYY-MM-DD), defaults to current date', example='2024-10-24'),
    'description': fields.String(description='Transaction notes (optional)', example='Lunch at restaurant'),
})

expense_update_model = api.model('TransactionUpdate', {
    'amount': fields.Float(description='Updated transaction amount', example=30.00),
    'category': fields.String(description='Updated spending category', example='Dining'),
    'date': fields.String(description='Updated transaction date (YYYY-MM-DD)', example='2024-10-24'),
    'description': fields.String(description='Updated transaction notes', example='Updated lunch'),
})

expense_list_model = api.model('TransactionCollection', {
    'expenses': fields.List(fields.Nested(expense_model)),
    'count': fields.Integer(description='Total transaction count')
})

message_model = api.model('OperationResponse', {
    'message': fields.String(description='Operation status message')
})

error_model = api.model('ErrorResponse', {
    'error': fields.String(description='Error details')
})

health_model = api.model('ServiceHealth', {
    'status': fields.String(description='Service health status'),
    'message': fields.String(description='Service status description')
})

csv_export_model = api.model('DataExport', {
    'message': fields.String(description='Export status message'),
    'data': fields.String(description='CSV formatted transaction data')
})

# Request parsers for query string parameters
transaction_filter_parser = reqparse.RequestParser()
transaction_filter_parser.add_argument('category', type=str, help='Filter transactions by category')
transaction_filter_parser.add_argument('date_from', type=str, help='Start date for filtering (YYYY-MM-DD)')
transaction_filter_parser.add_argument('date_to', type=str, help='End date for filtering (YYYY-MM-DD)')
transaction_filter_parser.add_argument('tag', type=str, help='Filter transactions by tag')

@ns_health.route('')
class ServiceHealthCheck(Resource):
    @ns_health.doc('check_service_status')
    @ns_health.marshal_with(health_model)
    def get(self):
        """Monitor API service health status"""
        return {
            'status': 'operational',
            'message': 'SpendSense Transaction API is fully operational'
        }

@ns_expenses.route('')
class TransactionCollection(Resource):
    @ns_expenses.doc('retrieve_transactions')
    @ns_expenses.expect(transaction_filter_parser)
    @ns_expenses.marshal_with(expense_list_model)
    def get(self):
        """Retrieve all transactions with optional filtering capabilities"""
        filter_args = transaction_filter_parser.parse_args()
        category_filter = filter_args['category']
        start_date = filter_args['date_from']
        end_date = filter_args['date_to']
        tag_filter = filter_args['tag']
        
        try:
            # Apply filters if any are specified
            if any([category_filter, start_date, end_date, tag_filter]):
                transaction_list = spend_controller.filter_expenses(category_filter, start_date, end_date, tag_filter)
            else:
                transaction_list = spend_controller.get_all_expenses()
            
            return {
                'expenses': [txn.to_dict() for txn in transaction_list],
                'count': len(transaction_list)
            }
        except Exception as e:
            api.abort(500, f'Server error occurred: {str(e)}')

    @ns_expenses.doc('record_transaction')
    @ns_expenses.expect(expense_input_model)
    @ns_expenses.marshal_with(expense_model, code=201)
    def post(self):
        """Record a new financial transaction"""
        try:
            payload = request.get_json()
            
            # Ensure all required fields are present
            mandatory_fields = ['amount', 'category', 'description']
            for field_name in mandatory_fields:
                if field_name not in payload:
                    api.abort(400, f'Required field missing: {field_name}')
            
            # Extract and set transaction data
            txn_amount = float(payload['amount'])
            txn_category = payload['category']
            txn_date = payload.get('date', datetime.now().strftime("%Y-%m-%d"))
            txn_description = payload['description']
            
            new_transaction = spend_controller.add_expense(txn_amount, txn_category, txn_date, txn_description)
            
            return new_transaction.to_dict(), 201
        except ValueError as e:
            api.abort(400, 'Amount must be a valid numeric value')
        except Exception as e:
            api.abort(500, f'Transaction creation failed: {str(e)}')

@ns_expenses.route('/<string:expense_id>')
@ns_expenses.param('expense_id', 'Transaction identifier')
class TransactionResource(Resource):
    @ns_expenses.doc('fetch_transaction_details')
    @ns_expenses.marshal_with(expense_model)
    def get(self, expense_id):
        """Retrieve detailed information for a specific transaction"""
        try:
            transaction = spend_controller.get_expense_by_id(expense_id)
            if transaction:
                return transaction.to_dict()
            else:
                api.abort(404, 'Transaction record not found')
        except Exception as e:
            api.abort(500, f'Retrieval failed: {str(e)}')

    @ns_expenses.doc('modify_transaction')
    @ns_expenses.expect(expense_update_model)
    @ns_expenses.marshal_with(expense_model)
    def put(self, expense_id):
        """Modify an existing transaction record"""
        try:
            payload = request.get_json()
            
            # Parse update fields from payload
            updated_amount = float(payload['amount']) if 'amount' in payload else None
            updated_category = payload.get('category')
            updated_date = payload.get('date')
            updated_description = payload.get('description')
            
            modified_transaction = spend_controller.update_expense(
                expense_id, updated_amount, updated_category, updated_date, updated_description
            )
            
            if modified_transaction:
                return modified_transaction.to_dict()
            else:
                api.abort(404, 'Transaction record not found')
        except ValueError as e:
            api.abort(400, 'Amount must be a valid numeric value')
        except Exception as e:
            api.abort(500, f'Update operation failed: {str(e)}')

    @ns_expenses.doc('remove_transaction')
    @ns_expenses.marshal_with(message_model)
    def delete(self, expense_id):
        """Remove a transaction from the system"""
        try:
            if spend_controller.delete_expense(expense_id):
                return {'message': 'Transaction removed successfully'}
            else:
                api.abort(404, 'Transaction record not found')
        except Exception as e:
            api.abort(500, f'Deletion failed: {str(e)}')

@ns_expenses.route('/export/csv')
class TransactionDataExport(Resource):
    @ns_expenses.doc('export_transaction_data')
    @ns_expenses.marshal_with(csv_export_model)
    def get(self):
        """Generate CSV export of all transaction records"""
        try:
            csv_content = spend_controller.export_to_csv()
            return {
                'message': 'Data export completed successfully',
                'data': csv_content
            }
        except Exception as e:
            api.abort(500, f'Export generation failed: {str(e)}')

# Global exception handler
@api.errorhandler
def handle_api_errors(error):
    """Centralized error handling for all API endpoints"""
    return {'error': str(error)}, getattr(error, 'code', 500)

# Application entry point
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)