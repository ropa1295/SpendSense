from models.budget_plan import BudgetPlan
from typing import List, Optional, Dict
from datetime import datetime

class SenseController:
    """
    Controller for managing budget awareness and financial planning.
    Tracks budgets by month and category, providing insights into spending patterns.
    """
    
    def __init__(self):
        self._budget_registry: List[BudgetPlan] = []
    
    def set_budget(self, amount: float, month: str, category: Optional[str] = None) -> BudgetPlan:
        """
        Create or update a budget entry for the specified time period.
        
        Args:
            amount: BudgetPlan amount to allocate
            month: Target month in YYYY-MM format
            category: Optional category filter (None for overall budget)
            
        Returns:
            The created or updated BudgetPlan instance
        """
        existing_budget = self._find_budget_by_criteria(month, category)
        
        if existing_budget:
            existing_budget.amount = amount
            return existing_budget
        
        new_budget = BudgetPlan(amount, month, category)
        self._budget_registry.append(new_budget)
        return new_budget
    
    def get_budget(self, month: str, category: Optional[str] = None) -> Optional[BudgetPlan]:
        """
        Retrieve a specific budget by month and optional category.
        
        Args:
            month: Target month in YYYY-MM format
            category: Optional category to filter by
            
        Returns:
            Matching BudgetPlan instance or None if not found
        """
        return self._find_budget_by_criteria(month, category)
    
    def get_all_budgets(self) -> List[BudgetPlan]:
        """Retrieve complete list of all registered budgets."""
        return list(self._budget_registry)
    
    def get_budgets_by_month(self, month: str) -> List[BudgetPlan]:
        """
        Fetch all budgets associated with a specific month.
        
        Args:
            month: Target month in YYYY-MM format
            
        Returns:
            List of BudgetPlan instances for the specified month
        """
        return [budget for budget in self._budget_registry if budget.month == month]
    
    def delete_budget(self, budget_id: str) -> bool:
        """
        Remove a budget from the registry by its unique identifier.
        
        Args:
            budget_id: Unique budget identifier
            
        Returns:
            True if budget was deleted, False if not found
        """
        matching_budget = self._find_budget_by_id(budget_id)
        if matching_budget:
            self._budget_registry.remove(matching_budget)
            return True
        return False
    
    def _find_budget_by_criteria(self, month: str, category: Optional[str] = None) -> Optional[BudgetPlan]:
        """Internal helper to locate budget by month and category."""
        for budget in self._budget_registry:
            if budget.month == month and budget.category == category:
                return budget
        return None
    
    def _find_budget_by_id(self, budget_id: str) -> Optional[BudgetPlan]:
        """Internal helper to locate budget by ID."""
        for budget in self._budget_registry:
            if budget.id == budget_id:
                return budget
        return None
    
    def calculate_spending_vs_budget(self, expenses: List, month: str) -> Dict:
        """
        Analyze spending patterns against budget allocations for a given month.
        Provides comprehensive breakdown by category and overall status.
        
        Args:
            expenses: Collection of Expense objects to analyze
            month: Target month in YYYY-MM format
            
        Returns:
            Dictionary containing detailed budget analysis metrics
        """
        # Extract expenses for target month
        filtered_expenses = [exp for exp in expenses if exp.date.startswith(month)]
        
        # Aggregate spending totals
        total_expenditure = sum(exp.amount for exp in filtered_expenses)
        
        # Build category-wise spending map
        category_spending = self._aggregate_by_category(filtered_expenses)
        
        # Retrieve month's budget allocations
        monthly_budgets = self.get_budgets_by_month(month)
        
        # Extract overall budget (category=None)
        overall_budget = self._find_budget_by_criteria(month, None)
        total_allocation = overall_budget.amount if overall_budget else 0
        
        # Analyze each category budget
        category_breakdown = self._analyze_category_budgets(
            monthly_budgets, 
            category_spending
        )
        
        # Calculate overall metrics
        budget_remainder = total_allocation - total_expenditure
        spending_ratio = (total_expenditure / total_allocation * 100) if total_allocation > 0 else 0
        budget_status = 'exceeded' if total_expenditure > total_allocation else 'within_limit'
        
        return {
            'month': month,
            'total_budget': total_allocation,
            'total_spent': total_expenditure,
            'total_remaining': budget_remainder,
            'total_percentage': spending_ratio,
            'status': budget_status,
            'categories': category_breakdown,
            'spending_by_category': category_spending
        }
    
    def _aggregate_by_category(self, expenses: List) -> Dict[str, float]:
        """Helper to sum expenses by category."""
        aggregation = {}
        for expense in expenses:
            category_key = expense.category
            if category_key not in aggregation:
                aggregation[category_key] = 0
            aggregation[category_key] += expense.amount
        return aggregation
    
    def _analyze_category_budgets(self, budgets: List[BudgetPlan], spending: Dict[str, float]) -> Dict:
        """Helper to compare category budgets against actual spending."""
        analysis = {}
        
        for budget in budgets:
            if not budget.category:  # Skip overall budget
                continue
                
            category_name = budget.category
            spent_amount = spending.get(category_name, 0)
            remaining_amount = budget.amount - spent_amount
            usage_percentage = (spent_amount / budget.amount * 100) if budget.amount > 0 else 0
            
            analysis[category_name] = {
                'budget': budget.amount,
                'spent': spent_amount,
                'remaining': remaining_amount,
                'percentage': usage_percentage,
                'status': 'exceeded' if spent_amount > budget.amount else 'within_limit'
            }
        
        return analysis
