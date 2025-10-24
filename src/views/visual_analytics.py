"""
Visual Analytics Module
Provides chart generation and data visualization for spending analysis.
"""

from matplotlib import pyplot as plt
from typing import List, Dict, Optional
from collections import defaultdict
import numpy as np


class SpendingVisualizer:
    """Generates visual analytics and charts for spending data."""
    
    def __init__(self):
        self._color_palette = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
            '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#52B788'
        ]
    
    def generate_category_bar_chart(self, transactions: List) -> None:
        """
        Create a bar chart showing spending by category.
        
        Args:
            transactions: List of transaction objects
        """
        if not transactions:
            print("⚠ No data available for chart generation.")
            return
        
        # Aggregate spending by category
        category_totals = self._aggregate_by_category(transactions)
        
        # Sort by amount descending
        sorted_categories = sorted(
            category_totals.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        categories = [item[0] for item in sorted_categories]
        amounts = [item[1] for item in sorted_categories]
        
        # Create figure
        plt.figure(figsize=(12, 7))
        bars = plt.bar(
            categories, 
            amounts, 
            color=self._color_palette[:len(categories)],
            edgecolor='white',
            linewidth=1.5
        )
        
        # Customize chart
        plt.title('Spending Analysis by Category', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Category', fontsize=12, fontweight='bold')
        plt.ylabel('Total Spent ($)', fontsize=12, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2., 
                height,
                f'${height:.2f}',
                ha='center', 
                va='bottom',
                fontsize=9,
                fontweight='bold'
            )
        
        plt.tight_layout()
        plt.show()
    
    def generate_category_pie_chart(self, transactions: List) -> None:
        """
        Create a pie chart showing spending distribution by category.
        
        Args:
            transactions: List of transaction objects
        """
        if not transactions:
            print("⚠ No data available for chart generation.")
            return
        
        # Aggregate spending by category
        category_totals = self._aggregate_by_category(transactions)
        
        # Sort by amount descending
        sorted_categories = sorted(
            category_totals.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        categories = [item[0] for item in sorted_categories]
        amounts = [item[1] for item in sorted_categories]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            amounts,
            labels=categories,
            autopct='%1.1f%%',
            startangle=90,
            colors=self._color_palette[:len(categories)],
            explode=[0.05] * len(categories),  # Slightly separate slices
            shadow=True
        )
        
        # Customize text
        for text in texts:
            text.set_fontsize(10)
            text.set_fontweight('bold')
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)
            autotext.set_fontweight('bold')
        
        ax.set_title('Spending Distribution by Category', fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.show()
    
    def generate_spending_trend(self, transactions: List) -> None:
        """
        Create a line chart showing spending trends over time.
        
        Args:
            transactions: List of transaction objects
        """
        if not transactions:
            print("⚠ No data available for chart generation.")
            return
        
        # Aggregate by date
        daily_spending = defaultdict(float)
        for txn in transactions:
            daily_spending[txn.date] += txn.amount
        
        # Sort by date
        sorted_dates = sorted(daily_spending.keys())
        amounts = [daily_spending[date] for date in sorted_dates]
        
        # Create figure
        plt.figure(figsize=(14, 7))
        
        plt.plot(
            range(len(sorted_dates)), 
            amounts, 
            marker='o', 
            linewidth=2,
            markersize=6,
            color='#4ECDC4',
            markerfacecolor='#FF6B6B',
            markeredgecolor='white',
            markeredgewidth=2
        )
        
        # Customize chart
        plt.title('Daily Spending Trend', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Date', fontsize=12, fontweight='bold')
        plt.ylabel('Amount Spent ($)', fontsize=12, fontweight='bold')
        plt.xticks(range(len(sorted_dates)), sorted_dates, rotation=45, ha='right')
        plt.grid(True, alpha=0.3, linestyle='--')
        
        # Add average line
        avg_spending = np.mean(amounts)
        plt.axhline(
            y=avg_spending, 
            color='red', 
            linestyle='--', 
            linewidth=2, 
            alpha=0.7,
            label=f'Average: ${avg_spending:.2f}'
        )
        
        plt.legend(fontsize=10)
        plt.tight_layout()
        plt.show()
    
    def _aggregate_by_category(self, transactions: List) -> Dict[str, float]:
        """
        Helper to aggregate transaction amounts by category.
        
        Args:
            transactions: List of transaction objects
            
        Returns:
            Dictionary mapping categories to total amounts
        """
        aggregation = defaultdict(float)
        for txn in transactions:
            aggregation[txn.category] += txn.amount
        return dict(aggregation)


# Legacy function wrapper for backward compatibility
_visualizer = SpendingVisualizer()

def generate_expense_chart(expenses):
    """Legacy wrapper for bar chart generation."""
    _visualizer.generate_category_bar_chart(expenses)
