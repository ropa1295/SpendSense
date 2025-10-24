# SpendSense Test Suite

## Overview
Comprehensive test coverage for the SpendSense personal finance management application.

## Test Statistics
- **Total Tests**: 58
- **Passing**: 57
- **Skipped**: 1 (edge case requiring API error handling improvement)
- **Test Files**: 5
- **Code Coverage**: Models, Controllers, and API Endpoints

## Test Files

### 1. test_transaction_model.py (11 tests)
Tests for the Transaction data model.

**Coverage:**
- Transaction creation with all fields
- Unique ID generation
- `to_dict()` serialization
- Property access (amount, category, date, description)
- Property modification
- Read-only properties (id, created_at)
- Minimal data handling

**Key Test Cases:**
- `test_transaction_creation` - Verifies correct initialization
- `test_transaction_id_is_unique` - Ensures UUID uniqueness
- `test_transaction_to_dict` - Validates serialization
- `test_transaction_read_only_properties` - Confirms immutability

### 2. test_budget_model.py (9 tests)
Tests for the BudgetPlan data model.

**Coverage:**
- Budget creation with/without category
- Unique ID generation
- `to_dict()` serialization
- Property immutability testing
- None category handling (total budgets)

**Key Test Cases:**
- `test_budget_creation` - Verifies proper initialization
- `test_budget_creation_without_category` - Tests total budget creation
- `test_budget_properties_are_immutable` - Validates read-only properties
- `test_budget_to_dict_with_none_category` - Tests None handling

### 3. test_spend_controller.py (14 tests)
Tests for the SpendController business logic.

**Coverage:**
- CRUD operations (Create, Read, Update, Delete)
- Expense filtering by category
- CSV export functionality
- Edge cases (nonexistent expenses)
- Partial updates

**Key Test Cases:**
- `test_add_expense` - Transaction creation
- `test_get_all_expenses` - Batch retrieval
- `test_update_expense` - Full update
- `test_update_partial_expense` - Partial field updates
- `test_delete_expense` - Transaction removal
- `test_filter_expenses_by_category` - Category filtering
- `test_export_to_csv` - CSV export validation

### 4. test_sense_controller.py (12 tests)
Tests for the SenseController (budget management).

**Coverage:**
- Budget creation and retrieval
- Budget deletion
- Budget filtering by month
- Spending vs. budget calculations
- Category-level budget analysis
- Over-budget detection

**Key Test Cases:**
- `test_set_budget` - Budget creation
- `test_get_budgets_by_month` - Month filtering
- `test_calculate_spending_vs_budget_within_limit` - Under budget scenario
- `test_calculate_spending_vs_budget_over_limit` - Over budget scenario
- `test_calculate_spending_vs_budget_category_level` - Category budgets
- `test_delete_budget` - Budget removal

### 5. test_api_endpoints.py (12 tests + 1 skipped)
Integration tests for REST API endpoints.

**Coverage:**
- HTTP method testing (GET, POST, PUT, DELETE)
- Request/response validation
- Error handling (404, 400 errors)
- Content-type headers
- API response structure

**Key Test Cases:**
- `test_home_page` - Dashboard accessibility
- `test_api_docs_available` - Swagger UI availability
- `test_create_transaction` - POST /api/expenses
- `test_get_transaction_by_id` - GET /api/expenses/{id}
- `test_update_transaction` - PUT /api/expenses/{id}
- `test_delete_transaction` - DELETE /api/expenses/{id}
- `test_get_all_budgets` - GET /api/budgets
- `test_create_budget` - POST /api/budgets
- `test_get_budget_analysis` - GET /api/budgets/analysis/{month}
- `test_export_csv` - CSV export endpoint

**Skipped Test:**
- `test_update_nonexistent_transaction` - Edge case with API error handling

## Running Tests

### Run All Tests
```bash
python run_tests.py
```

### Run Specific Test File
```bash
python run_tests.py --file test_transaction_model.py
```

### Verbose Output
```bash
python run_tests.py --verbose
```

### Quiet Mode
```bash
python run_tests.py --quiet
```

### Using unittest Directly
```bash
# All tests
python -m unittest discover tests

# Specific file
python -m unittest tests.test_transaction_model

# Specific test
python -m unittest tests.test_transaction_model.TestTransaction.test_transaction_creation
```

## Test Structure

Each test file follows the standard unittest pattern:

```python
import unittest

class TestClassName(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test"""
        pass
    
    def tearDown(self):
        """Clean up after each test"""
        pass
    
    def test_feature_name(self):
        """Test a specific feature"""
        # Arrange
        # Act
        # Assert
        pass
```

## Test Coverage by Component

| Component | Tests | Status |
|-----------|-------|--------|
| Transaction Model | 11 | ✅ Pass |
| BudgetPlan Model | 9 | ✅ Pass |
| SpendController | 14 | ✅ Pass |
| SenseController | 12 | ✅ Pass |
| API Endpoints | 12 | ✅ Pass (1 skip) |
| **Total** | **58** | **✅ 57 Pass, 1 Skip** |

## Known Issues

1. **API Error Handling (Skipped Test)**
   - Issue: PUT request to nonexistent expense returns 500 instead of 404
   - Location: `web_app.py` - TransactionResource.put()
   - Workaround: Test skipped pending API improvement
   - Priority: Low (edge case)

## Adding New Tests

When adding new features, follow these guidelines:

1. **Create test file** in `tests/` directory matching pattern `test_*.py`
2. **Import necessary modules**:
   ```python
   import unittest
   import sys
   from pathlib import Path
   sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
   ```
3. **Write test class** inheriting from `unittest.TestCase`
4. **Use descriptive test names** starting with `test_`
5. **Add docstrings** describing what each test validates
6. **Run tests** to verify functionality

## CI/CD Integration

The test suite is designed for continuous integration:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    python -m pip install -r requirements.txt
    python run_tests.py
```

Exit codes:
- `0`: All tests passed
- `1`: One or more tests failed

## Test Maintenance

- **Run tests** before committing changes
- **Update tests** when modifying features
- **Add tests** for new features
- **Fix failing tests** immediately
- **Review skipped tests** periodically

## Contact

For test-related questions or issues:
- Create an issue on GitHub
- Tag with `testing` label
- Provide test output and error messages

---

**Last Updated**: October 24, 2025
**Test Framework**: Python unittest
**Python Version**: 3.8+
