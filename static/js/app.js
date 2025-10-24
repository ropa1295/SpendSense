const API_BASE = '/api';
let editingExpenseId = null;
let currentBudgetMonth = '';
let selectedMonth = new Date(); // Track the selected month for navigation

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setDefaultDate();
    setDefaultBudgetMonth();
    updateMonthDisplay();
    loadExpenses();
    loadStats();
    loadChart();
    loadTrendChart();
    
    document.getElementById('expenseForm').addEventListener('submit', handleSubmit);
    document.getElementById('cancelBtn').addEventListener('click', cancelEdit);
    document.getElementById('budgetForm').addEventListener('submit', handleBudgetSubmit);
});

function setDefaultDate() {
    const dateInput = document.getElementById('date');
    const today = new Date().toISOString().split('T')[0];
    dateInput.value = today;
}

function setDefaultBudgetMonth() {
    const monthInput = document.getElementById('budgetMonth');
    const today = new Date();
    const currentMonth = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}`;
    monthInput.value = currentMonth;
    currentBudgetMonth = currentMonth;
}

// Tab Navigation
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab and activate button
    const tabMap = {
        'home': 0,
        'transactions': 1,
        'goals': 2,
        'history': 3,
        'reports': 4,
        'settings': 5,
        'budget': 1 // Map budget to transactions for now
    };
    
    if (tabName === 'transactions' || tabName === 'expenses') {
        document.getElementById('transactionsTab').classList.add('active');
        document.querySelectorAll('.nav-btn')[0].classList.add('active');
        loadExpenses();
        loadStats();
        loadChart();
    } else if (tabName === 'goals') {
        document.getElementById('goalsTab').classList.add('active');
        document.querySelectorAll('.nav-btn')[1].classList.add('active');
        loadGoals();
    } else if (tabName === 'history') {
        document.getElementById('historyTab').classList.add('active');
        document.querySelectorAll('.nav-btn')[2].classList.add('active');
        loadHistoryData();
    } else if (tabName === 'budget') {
        document.getElementById('budgetTab')?.classList.add('active');
        document.querySelectorAll('.nav-btn')[0].classList.add('active');
        loadBudgetData();
    }
}

// Modal Functions
function toggleExpenseModal() {
    const modal = document.getElementById('expenseModal');
    if (modal.style.display === 'none' || !modal.style.display) {
        modal.style.display = 'flex';
        cancelEdit(); // Reset form
    } else {
        modal.style.display = 'none';
        cancelEdit();
    }
}

// Month Navigation
function updateMonthDisplay() {
    const monthEl = document.getElementById('currentMonth');
    if (monthEl) {
        const monthName = selectedMonth.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
        monthEl.textContent = monthName;
    }
}

function previousMonth() {
    // Go back one month
    selectedMonth = new Date(selectedMonth.getFullYear(), selectedMonth.getMonth() - 1, 1);
    updateMonthDisplay();
    // Reload data for the new month
    loadExpenses();
    loadStats();
    loadChart();
}

function nextMonth() {
    // Go forward one month
    selectedMonth = new Date(selectedMonth.getFullYear(), selectedMonth.getMonth() + 1, 1);
    updateMonthDisplay();
    // Reload data for the new month
    loadExpenses();
    loadStats();
    loadChart();
}

// Expense Functions
async function loadExpenses() {
    try {
        const response = await fetch(`${API_BASE}/expenses`);
        const data = await response.json();
        console.log('Loaded expenses:', data);
        
        // Filter expenses by selected month
        const targetMonth = selectedMonth.getMonth();
        const targetYear = selectedMonth.getFullYear();
        
        const filteredExpenses = data.expenses.filter(expense => {
            const expenseDate = new Date(expense.date);
            return expenseDate.getMonth() === targetMonth && 
                   expenseDate.getFullYear() === targetYear;
        });
        
        displayExpenses(filteredExpenses);
    } catch (error) {
        console.error('Error loading expenses:', error);
        showError('Failed to load expenses');
    }
}

function displayExpenses(expenses) {
    const container = document.getElementById('expensesList');
    
    if (!expenses || expenses.length === 0) {
        container.innerHTML = '<p class="no-data">No transactions yet</p>';
        return;
    }
    
    // Get category icons
    const categoryIcons = {
        'Groceries': '🛒',
        'Dining Out': '🍽️',
        'Coffee/Snacks': '☕',
        'Rent/Mortgage': '🏠',
        'Utilities': '💡',
        'Fuel/Gas': '⛽',
        'Public Transit': '🚇',
        'Entertainment': '🎬',
        'Shopping/Clothing': '🛍️',
        'Health Insurance': '🏥',
        'Medical Expenses': '💊',
        'Gym/Fitness': '💪',
        'default': '💰'
    };
    
    container.innerHTML = expenses.map(expense => {
        const icon = categoryIcons[expense.category] || categoryIcons['default'];
        const date = new Date(expense.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        
        return `
            <div class="transaction-item">
                <div class="transaction-icon">${icon}</div>
                <div class="transaction-details">
                    <div class="transaction-name">${expense.category}</div>
                    <div class="transaction-date">${date}</div>
                </div>
                <div class="transaction-amount negative">$${parseFloat(expense.amount).toFixed(2)}</div>
                <button class="icon-btn-small" onclick="editExpense('${expense.id}')">→</button>
            </div>
        `;
    }).join('');
}

async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/expenses`);
        const data = await response.json();
        const expenses = data.expenses || [];
        
        // Get selected month and year
        const targetMonth = selectedMonth.getMonth();
        const targetYear = selectedMonth.getFullYear();
        
        // Filter expenses for selected month only
        const monthExpenses = expenses.filter(expense => {
            const expenseDate = new Date(expense.date);
            return expenseDate.getMonth() === targetMonth && 
                   expenseDate.getFullYear() === targetYear;
        });
        
        // Calculate selected month's total
        const monthTotal = monthExpenses.reduce((sum, expense) => {
            return sum + parseFloat(expense.amount || 0);
        }, 0);
        
        console.log(`Expenses for ${selectedMonth.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}:`, monthTotal);
        
        // Update sidebar stats with selected month total
        const totalEl = document.getElementById('totalExpenses');
        if (totalEl) {
            totalEl.textContent = `$${monthTotal.toFixed(2)}`;
        }
        
        // Update financial health meter with selected month total
        const netPositionEl = document.getElementById('netPosition');
        if (netPositionEl) {
            netPositionEl.textContent = `$${monthTotal.toFixed(2)}`;
        }
        
        // Update month expenses if exists
        const monthEl = document.getElementById('monthExpenses');
        if (monthEl) {
            monthEl.textContent = `$${monthTotal.toFixed(2)}`;
        }
        
        // Calculate and update average daily spend for selected month
        await calculateAverageDailySpend();
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function calculateAverageDailySpend() {
    try {
        const response = await fetch(`${API_BASE}/expenses`);
        const data = await response.json();
        const expenses = data.expenses || [];
        
        // Get selected month and year
        const targetMonth = selectedMonth.getMonth();
        const targetYear = selectedMonth.getFullYear();
        const now = new Date();
        const isCurrentMonth = targetMonth === now.getMonth() && targetYear === now.getFullYear();
        
        // For current month, use current day; for past months, use last day of month
        const daysInMonth = isCurrentMonth ? now.getDate() : new Date(targetYear, targetMonth + 1, 0).getDate();
        
        // Filter expenses for selected month
        const monthExpenses = expenses.filter(expense => {
            const expenseDate = new Date(expense.date);
            return expenseDate.getMonth() === targetMonth && 
                   expenseDate.getFullYear() === targetYear;
        });
        
        // Calculate total for selected month
        const monthTotal = monthExpenses.reduce((sum, expense) => {
            return sum + parseFloat(expense.amount || 0);
        }, 0);
        
        // Calculate average per day
        const averagePerDay = daysInMonth > 0 ? monthTotal / daysInMonth : 0;
        
        // Update the display
        const avgDailyEl = document.getElementById('averageDailySpend');
        if (avgDailyEl) {
            avgDailyEl.textContent = `$${averagePerDay.toFixed(2)}`;
        }
        
        // Calculate trend (compare with previous month)
        const lastMonth = targetMonth === 0 ? 11 : targetMonth - 1;
        const lastMonthYear = targetMonth === 0 ? targetYear - 1 : targetYear;
        
        const lastMonthExpenses = expenses.filter(expense => {
            const expenseDate = new Date(expense.date);
            return expenseDate.getMonth() === lastMonth && 
                   expenseDate.getFullYear() === lastMonthYear;
        });
        
        const lastMonthTotal = lastMonthExpenses.reduce((sum, expense) => {
            return sum + parseFloat(expense.amount || 0);
        }, 0);
        
        // Get days in last month
        const lastMonthDate = new Date(lastMonthYear, lastMonth + 1, 0);
        const daysInLastMonth = lastMonthDate.getDate();
        const lastMonthAverage = daysInLastMonth > 0 ? lastMonthTotal / daysInLastMonth : 0;
        
        // Update trend indicator
        const trendEl = document.getElementById('spendingTrend');
        if (trendEl) {
            const difference = averagePerDay - lastMonthAverage;
            const percentChange = lastMonthAverage > 0 ? ((difference / lastMonthAverage) * 100).toFixed(1) : 0;
            
            let trendHTML = '';
            if (Math.abs(difference) < 0.5) {
                trendHTML = '<span class="trend-indicator neutral">→</span><span class="trend-text">No change from last month</span>';
            } else if (difference > 0) {
                trendHTML = `<span class="trend-indicator up">↑</span><span class="trend-text">Up ${percentChange}% from last month</span>`;
            } else {
                trendHTML = `<span class="trend-indicator down">↓</span><span class="trend-text">Down ${Math.abs(percentChange)}% from last month</span>`;
            }
            
            trendEl.innerHTML = trendHTML;
        }
        
    } catch (error) {
        console.error('Error calculating average daily spend:', error);
    }
}

async function loadChart() {
    try {
        // Pass month and year parameters to filter chart data
        const month = selectedMonth.getMonth() + 1; // API expects 1-12
        const year = selectedMonth.getFullYear();
        const response = await fetch(`${API_BASE}/chart/category?month=${month}&year=${year}`);
        if (response.ok) {
            const blob = await response.blob();
            const imgUrl = URL.createObjectURL(blob);
            document.getElementById('categoryChart').src = imgUrl;
            document.getElementById('categoryChart').style.display = 'block';
            document.getElementById('noChartData').style.display = 'none';
        }
        
        // Load category breakdown for the selected month
        await loadCategoryBreakdown();
    } catch (error) {
        console.error('Error loading chart:', error);
    }
}

// Load Category Breakdown for Selected Month
async function loadCategoryBreakdown() {
    try {
        const response = await fetch(`${API_BASE}/expenses`);
        const data = await response.json();
        const expenses = data.expenses || [];
        
        // Filter expenses for selected month
        const targetMonth = selectedMonth.getMonth();
        const targetYear = selectedMonth.getFullYear();
        
        const monthExpenses = expenses.filter(expense => {
            const expenseDate = new Date(expense.date);
            return expenseDate.getMonth() === targetMonth && 
                   expenseDate.getFullYear() === targetYear;
        });
        
        // Calculate category totals
        const categoryTotals = {};
        let total = 0;
        
        monthExpenses.forEach(expense => {
            const category = expense.category || 'Uncategorized';
            const amount = parseFloat(expense.amount || 0);
            categoryTotals[category] = (categoryTotals[category] || 0) + amount;
            total += amount;
        });
        
        // Sort categories by amount
        const sortedCategories = Object.entries(categoryTotals)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5); // Top 5 categories
        
        // Check if there's any data
        const spendingBreakdownCard = document.querySelector('.spending-breakdown');
        if (sortedCategories.length === 0 || total === 0) {
            // Hide the entire Spending Breakdown card if no data
            if (spendingBreakdownCard) {
                spendingBreakdownCard.style.display = 'none';
            }
        } else {
            // Show the card if there's data
            if (spendingBreakdownCard) {
                spendingBreakdownCard.style.display = 'block';
            }
            // Draw bar chart for top categories
            drawTopCategoriesChart(sortedCategories, total);
        }
        
    } catch (error) {
        console.error('Error loading category breakdown:', error);
    }
}

// Draw Top Categories Bar Chart
function drawTopCategoriesChart(categories, total) {
    const canvas = document.getElementById('barChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    if (categories.length === 0) {
        ctx.fillStyle = '#a0aec0';
        ctx.font = '14px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText('No data available', width / 2, height / 2);
        return;
    }
    
    const padding = { top: 20, right: 80, bottom: 40, left: 150 };
    const chartHeight = height - padding.top - padding.bottom;
    const barHeight = Math.min(25, chartHeight / categories.length - 10);
    const maxAmount = Math.max(...categories.map(c => c[1]));
    
    categories.forEach(([category, amount], index) => {
        const barWidth = ((amount / maxAmount) * (width - padding.left - padding.right));
        const y = padding.top + index * (barHeight + 15);
        
        // Draw bar
        ctx.fillStyle = index === 0 ? '#2c5f5d' : '#5fc3b4';
        ctx.fillRect(padding.left, y, barWidth, barHeight);
        
        // Draw full category name (left side)
        ctx.fillStyle = '#4a5568';
        ctx.font = '13px sans-serif';
        ctx.textAlign = 'right';
        // Don't truncate - show full category name
        ctx.fillText(category, padding.left - 10, y + barHeight / 2 + 5);
        
        // Draw amount label (right side of bar)
        ctx.fillStyle = '#2d3748';
        ctx.font = 'bold 13px sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText(`$${amount.toFixed(2)}`, padding.left + barWidth + 8, y + barHeight / 2 + 5);
    });
}

async function handleSubmit(e) {
    e.preventDefault();
    
    const amount = parseFloat(document.getElementById('amount').value);
    const category = document.getElementById('category').value;
    const date = document.getElementById('date').value;
    const description = document.getElementById('description').value;
    
    const expenseData = { 
        amount: amount, 
        category: category, 
        date: date, 
        description: description, 
        tags: [] 
    };
    
    console.log('Submitting expense:', expenseData);
    
    try {
        let response;
        if (editingExpenseId) {
            response = await fetch(`${API_BASE}/expenses/${editingExpenseId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(expenseData)
            });
        } else {
            response = await fetch(`${API_BASE}/expenses`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(expenseData)
            });
        }
        
        console.log('Response status:', response.status);
        const data = await response.json();
        console.log('Response data:', data);
        
        if (response.ok && data.success) {
            toggleExpenseModal(); // Close modal
            resetForm();
            await loadExpenses();
            await loadStats();
            await loadChart();
            await loadTrendChart();
            showSuccess(editingExpenseId ? 'Expense updated!' : 'Expense added!');
        } else {
            showError(data.error || data.message || 'Failed to save expense');
        }
    } catch (error) {
        console.error('Error saving expense:', error);
        showError('Failed to save expense: ' + error.message);
    }
}

async function editExpense(id) {
    try {
        const response = await fetch(`${API_BASE}/expenses`);
        const data = await response.json();
        const expense = data.expenses.find(e => e.id === id);
        
        if (expense) {
            editingExpenseId = id;
            document.getElementById('expenseId').value = id;
            document.getElementById('amount').value = expense.amount;
            document.getElementById('category').value = expense.category;
            document.getElementById('date').value = expense.date;
            document.getElementById('description').value = expense.description;
            
            // Only update tags field if it exists
            const tagsField = document.getElementById('tags');
            if (tagsField) {
                tagsField.value = (expense.tags || []).join(', ');
            }
            
            document.getElementById('formTitle').textContent = 'Edit Expense';
            document.getElementById('submitBtn').textContent = 'Update Expense';
            
            // Only update cancelBtn if it exists
            const cancelBtn = document.getElementById('cancelBtn');
            if (cancelBtn) {
                cancelBtn.style.display = 'block';
            }
            
            // Open modal if it exists, otherwise scroll to form
            const modal = document.getElementById('expenseModal');
            if (modal) {
                modal.style.display = 'flex';
            } else {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        }
    } catch (error) {
        console.error('Error loading expense:', error);
        showError('Failed to load expense');
    }
}

async function deleteExpense(id) {
    if (!confirm('Are you sure you want to delete this expense?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/expenses/${id}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        console.log('Delete response:', data);
        
        if (response.ok && data.success) {
            await loadExpenses();
            await loadStats();
            await loadChart();
            await loadTrendChart();
            // Reload budget data if on budget tab
            if (document.getElementById('budgetTab').classList.contains('active')) {
                await loadBudgetData();
            }
            showSuccess('Expense deleted!');
        } else {
            showError(data.error || 'Failed to delete expense');
        }
    } catch (error) {
        console.error('Error deleting expense:', error);
        showError('Failed to delete expense');
    }
}

// Reset current month's expenses
async function resetMonthBudget() {
    const monthName = selectedMonth.toLocaleString('en-US', { month: 'long', year: 'numeric' });
    
    if (!confirm(`Are you sure you want to delete ALL expenses from ${monthName}? This action cannot be undone!`)) {
        return;
    }
    
    try {
        // Get all expenses
        const response = await fetch(`${API_BASE}/expenses`);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error('Failed to fetch expenses');
        }
        
        const expenses = data.expenses || data;
        
        // Filter expenses for the selected month
        const year = selectedMonth.getFullYear();
        const month = selectedMonth.getMonth() + 1;
        
        const monthExpenses = expenses.filter(expense => {
            const expenseDate = new Date(expense.date);
            return expenseDate.getFullYear() === year && (expenseDate.getMonth() + 1) === month;
        });
        
        if (monthExpenses.length === 0) {
            showError(`No expenses found for ${monthName}`);
            return;
        }
        
        // Delete each expense
        let deletedCount = 0;
        let failedCount = 0;
        
        for (const expense of monthExpenses) {
            try {
                const deleteResponse = await fetch(`${API_BASE}/expenses/${expense.id}`, {
                    method: 'DELETE'
                });
                
                if (deleteResponse.ok) {
                    deletedCount++;
                } else {
                    failedCount++;
                }
            } catch (error) {
                console.error(`Failed to delete expense ${expense.id}:`, error);
                failedCount++;
            }
        }
        
        // Reload all data
        await loadExpenses();
        await loadStats();
        await loadChart();
        await loadCategoryBreakdown();
        
        if (deletedCount > 0) {
            showSuccess(`Successfully deleted ${deletedCount} expense(s) from ${monthName}`);
        }
        
        if (failedCount > 0) {
            showError(`Failed to delete ${failedCount} expense(s)`);
        }
        
    } catch (error) {
        console.error('Error resetting month budget:', error);
        showError('Failed to reset month budget');
    }
}

function cancelEdit() {
    resetForm();
}

function resetForm() {
    editingExpenseId = null;
    document.getElementById('expenseForm').reset();
    document.getElementById('expenseId').value = '';
    document.getElementById('formTitle').textContent = 'Add New Expense';
    document.getElementById('submitBtn').textContent = 'Add Expense';
    
    // Only update cancelBtn if it exists (for old layout compatibility)
    const cancelBtn = document.getElementById('cancelBtn');
    if (cancelBtn) {
        cancelBtn.style.display = 'none';
    }
    
    setDefaultDate();
}

async function filterExpenses() {
    const category = document.getElementById('filterCategory').value;
    const tag = document.getElementById('filterTag').value;
    
    let url = `${API_BASE}/expenses?`;
    if (category) url += `category=${encodeURIComponent(category)}&`;
    if (tag) url += `tag=${encodeURIComponent(tag)}`;
    
    try {
        const response = await fetch(url);
        const data = await response.json();
        displayExpenses(data.expenses);
    } catch (error) {
        console.error('Error filtering expenses:', error);
        showError('Failed to filter expenses');
    }
}

function clearFilters() {
    document.getElementById('filterCategory').value = '';
    document.getElementById('filterTag').value = '';
    loadExpenses();
}

async function exportCSV() {
    try {
        const response = await fetch(`${API_BASE}/expenses/export/csv`);
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `expenses_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        showSuccess('CSV exported successfully!');
    } catch (error) {
        console.error('Error exporting CSV:', error);
        showError('Failed to export CSV');
    }
}

// Budget Functions
async function loadBudgetData() {
    const month = document.getElementById('budgetMonth').value;
    currentBudgetMonth = month;
    
    try {
        // Load budget analysis
        const response = await fetch(`${API_BASE}/budgets/analysis/${month}`);
        const data = await response.json();
        console.log('Budget analysis:', data);
        
        // Update stats
        document.getElementById('totalBudget').textContent = `$${parseFloat(data.total_budget || 0).toFixed(2)}`;
        document.getElementById('totalSpent').textContent = `$${parseFloat(data.total_spent || 0).toFixed(2)}`;
        
        const remaining = data.total_remaining || 0;
        const remainingEl = document.getElementById('totalRemaining');
        remainingEl.textContent = `$${Math.abs(remaining).toFixed(2)}`;
        remainingEl.className = 'stat-value ' + (remaining < 0 ? 'over-budget' : 'under-budget');
        
        const statusEl = document.getElementById('budgetStatus');
        if (data.total_budget === 0) {
            statusEl.textContent = 'Not Set';
            statusEl.className = 'stat-value';
        } else {
            statusEl.textContent = data.status === 'over' ? '⚠️ Over' : '✅ Under';
            statusEl.className = 'stat-value ' + (data.status === 'over' ? 'over-budget' : 'under-budget');
        }
        
        // Display category budgets
        displayCategoryBudgets(data.categories);
        
        // Load budget chart
        await loadBudgetChart(month);
        
        // Load trend chart
        await loadTrendChart();
        
    } catch (error) {
        console.error('Error loading budget data:', error);
        showError('Failed to load budget data');
    }
}

function displayCategoryBudgets(categories) {
    const container = document.getElementById('categoryBudgetsList');
    
    if (!categories || Object.keys(categories).length === 0) {
        container.innerHTML = '<p class="no-data">No category budgets set</p>';
        return;
    }
    
    container.innerHTML = Object.entries(categories).map(([category, data]) => {
        const percentage = data.percentage;
        const isOver = data.status === 'over';
        const isWarning = percentage > 80 && !isOver;
        const progressClass = isOver ? 'over-budget' : (isWarning ? 'warning' : '');
        const progressWidth = Math.min(percentage, 100);
        
        return `
            <div class="budget-item">
                <div class="budget-item-header">
                    <span class="budget-category-name">${category}</span>
                    <span class="budget-amount">$${data.budget.toFixed(2)}</span>
                </div>
                <div class="budget-progress">
                    <div class="progress-bar">
                        <div class="progress-fill ${progressClass}" style="width: ${progressWidth}%">
                            ${percentage.toFixed(0)}%
                        </div>
                    </div>
                    <div class="budget-details">
                        <span>Spent: $${data.spent.toFixed(2)}</span>
                        <span>Remaining: $${Math.abs(data.remaining).toFixed(2)}</span>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

async function handleBudgetSubmit(e) {
    e.preventDefault();
    
    const amount = parseFloat(document.getElementById('budgetAmount').value);
    const category = document.getElementById('budgetCategory').value || null;
    const month = currentBudgetMonth;
    
    const budgetData = {
        amount: amount,
        month: month,
        category: category
    };
    
    console.log('Setting budget:', budgetData);
    
    try {
        const response = await fetch(`${API_BASE}/budgets`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(budgetData)
        });
        
        const data = await response.json();
        console.log('Budget response:', data);
        
        if (response.ok && data.success) {
            document.getElementById('budgetForm').reset();
            await loadBudgetData();
            showSuccess('Budget set successfully!');
        } else {
            showError(data.error || 'Failed to set budget');
        }
    } catch (error) {
        console.error('Error setting budget:', error);
        showError('Failed to set budget: ' + error.message);
    }
}

async function loadBudgetChart(month) {
    try {
        const response = await fetch(`${API_BASE}/chart/budget/${month}`);
        if (response.ok) {
            const blob = await response.blob();
            const imgUrl = URL.createObjectURL(blob);
            document.getElementById('budgetChart').src = imgUrl;
            document.getElementById('budgetChart').style.display = 'block';
            document.getElementById('noBudgetChart').style.display = 'none';
        }
    } catch (error) {
        console.error('Error loading budget chart:', error);
    }
}

async function loadTrendChart() {
    try {
        const response = await fetch(`${API_BASE}/chart/monthly-trend`);
        if (response.ok) {
            const blob = await response.blob();
            const imgUrl = URL.createObjectURL(blob);
            document.getElementById('trendChart').src = imgUrl;
            document.getElementById('trendChart').style.display = 'block';
            document.getElementById('noTrendChart').style.display = 'none';
        }
    } catch (error) {
        console.error('Error loading trend chart:', error);
    }
}

// Utility Functions
function showSuccess(message) {
    alert(`✅ ${message}`);
}

function showError(message) {
    alert(`❌ ${message}`);
}
// Goals Management
let goals = [];
let editingGoalId = null;

// Toggle Goal Modal
function toggleGoalModal() {
    const modal = document.getElementById('goalModal');
    if (modal.style.display === 'none' || !modal.style.display) {
        modal.style.display = 'flex';
    } else {
        modal.style.display = 'none';
        resetGoalForm();
    }
}

// Load Goals
function loadGoals() {
    // Load from localStorage
    const storedGoals = localStorage.getItem('financialGoals');
    if (storedGoals) {
        goals = JSON.parse(storedGoals);
    }
    displayGoals();
    displayDashboardGoals();
    updateGoalStats();
}

// Display Goals in Dashboard Card
function displayDashboardGoals() {
    const dashboardList = document.getElementById('dashboardGoalsList');
    if (!dashboardList) return;
    
    const activeGoals = goals.filter(g => !g.completed);
    
    if (activeGoals.length === 0) {
        dashboardList.innerHTML = '<p class="no-data">No active goals. Set your first goal!</p>';
    } else {
        // Show top 2 active goals
        const topGoals = activeGoals.slice(0, 2);
        dashboardList.innerHTML = topGoals.map(goal => createDashboardGoalItem(goal)).join('');
    }
}

// Create Dashboard Goal Item (compact version)
function createDashboardGoalItem(goal) {
    const percentage = Math.min(Math.round((goal.current / goal.target) * 100), 100);
    const status = getGoalStatus(goal);
    const deadline = new Date(goal.deadline).toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
    
    return `
        <div class="dashboard-goal-item">
            <div class="dashboard-goal-header">
                <span class="goal-icon-small">${goal.icon}</span>
                <div class="dashboard-goal-info">
                    <div class="dashboard-goal-name">${goal.name}</div>
                    <div class="dashboard-goal-amount">$${goal.current.toFixed(2)} / $${goal.target.toFixed(2)}</div>
                </div>
            </div>
            <div class="dashboard-goal-progress">
                <div class="goal-progress-bar small">
                    <div class="goal-progress-fill ${status.class}" style="width: ${percentage}%"></div>
                </div>
                <span class="dashboard-goal-percentage">${percentage}%</span>
            </div>
            <div class="dashboard-goal-deadline">Target: ${deadline}</div>
        </div>
    `;
}

// Display Goals
function displayGoals() {
    const activeList = document.getElementById('activeGoalsList');
    const completedList = document.getElementById('completedGoalsList');
    
    const activeGoals = goals.filter(g => !g.completed);
    const completedGoals = goals.filter(g => g.completed);
    
    // Active Goals
    if (activeGoals.length === 0) {
        activeList.innerHTML = '<p class="no-data">No active goals. Set your first goal!</p>';
    } else {
        activeList.innerHTML = activeGoals.map(goal => createGoalCard(goal)).join('');
    }
    
    // Completed Goals
    if (completedGoals.length === 0) {
        completedList.innerHTML = '<p class="no-data">No completed goals yet</p>';
    } else {
        completedList.innerHTML = completedGoals.map(goal => createGoalCard(goal)).join('');
    }
}

// Create Goal Card HTML
function createGoalCard(goal) {
    const percentage = Math.min(Math.round((goal.current / goal.target) * 100), 100);
    const status = getGoalStatus(goal);
    const deadline = new Date(goal.deadline).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    
    return `
        <div class="goal-card">
            <div class="goal-card-header">
                <div class="goal-icon-large">${goal.icon}</div>
                <div class="goal-info">
                    <div class="goal-name">${goal.name}</div>
                    <div class="goal-amounts">
                        <span class="current">$${goal.current.toFixed(2)}</span> of $${goal.target.toFixed(2)}
                    </div>
                </div>
            </div>
            
            <div class="goal-status ${status.class}">${status.icon} ${status.text}</div>
            
            <div class="goal-progress-section">
                <div class="goal-progress-bar">
                    <div class="goal-progress-fill ${status.class}" style="width: ${percentage}%"></div>
                </div>
                <div class="goal-percentage">achieved (${percentage}%)</div>
            </div>
            
            <div class="goal-deadline">Est. ${deadline}</div>
            
            <div class="goal-actions">
                <button class="goal-action-btn" onclick="editGoal('${goal.id}')">View Details</button>
                ${goal.completed ? 
                    '<button class="goal-action-btn" onclick="deleteGoal(\'' + goal.id + '\')">Delete</button>' :
                    '<button class="goal-action-btn primary" onclick="addContribution(\'' + goal.id + '\')">Add Contribution</button>'
                }
                ${!goal.completed && percentage >= 100 ? 
                    '<button class="goal-action-btn complete" onclick="completeGoal(\'' + goal.id + '\')">Mark Complete</button>' :
                    ''
                }
            </div>
        </div>
    `;
}

// Get Goal Status
function getGoalStatus(goal) {
    const percentage = (goal.current / goal.target) * 100;
    const today = new Date();
    const deadline = new Date(goal.deadline);
    const daysLeft = Math.ceil((deadline - today) / (1000 * 60 * 60 * 24));
    
    if (goal.completed || percentage >= 100) {
        return { class: 'achieved', icon: '✓', text: 'Achieved' };
    } else if (daysLeft < 0) {
        return { class: 'behind', icon: '⚠', text: 'Behind Pace - Est. Next Month' };
    } else if (daysLeft < 30 && percentage < 80) {
        return { class: 'behind', icon: '⚠', text: 'Behind Pace' };
    } else {
        return { class: 'on-track', icon: '●', text: `On Track - Est. ${deadline.toLocaleDateString('en-US', {month: 'short', year: 'numeric'})}` };
    }
}

// Update Goal Stats
function updateGoalStats() {
    const totalTarget = goals.reduce((sum, g) => sum + g.target, 0);
    const achievedCount = goals.filter(g => g.completed).length;
    
    document.getElementById('totalGoalTarget').textContent = `$${totalTarget.toFixed(0)}`;
    document.getElementById('achievedGoalsCount').textContent = achievedCount;
}

// Handle Goal Form Submit
document.addEventListener('DOMContentLoaded', () => {
    const goalForm = document.getElementById('goalForm');
    if (goalForm) {
        goalForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const goalData = {
                id: editingGoalId || Date.now().toString(),
                name: document.getElementById('goalName').value,
                target: parseFloat(document.getElementById('goalTarget').value),
                current: parseFloat(document.getElementById('goalCurrent').value),
                deadline: document.getElementById('goalDeadline').value,
                icon: document.getElementById('goalIcon').value,
                completed: false,
                createdAt: new Date().toISOString()
            };
            
            if (editingGoalId) {
                const index = goals.findIndex(g => g.id === editingGoalId);
                goals[index] = { ...goals[index], ...goalData };
            } else {
                goals.push(goalData);
            }
            
            localStorage.setItem('financialGoals', JSON.stringify(goals));
            toggleGoalModal();
            loadGoals();
        });
    }
    
    // Load goals on page load
    loadGoals();
});

// Add Contribution
function addContribution(goalId) {
    const amount = prompt('Enter contribution amount:');
    if (amount && !isNaN(amount)) {
        const goal = goals.find(g => g.id === goalId);
        if (goal) {
            goal.current += parseFloat(amount);
            localStorage.setItem('financialGoals', JSON.stringify(goals));
            loadGoals();
        }
    }
}

// Complete Goal
function completeGoal(goalId) {
    const goal = goals.find(g => g.id === goalId);
    if (goal) {
        goal.completed = true;
        goal.current = goal.target;
        localStorage.setItem('financialGoals', JSON.stringify(goals));
        loadGoals();
    }
}

// Delete Goal
function deleteGoal(goalId) {
    if (confirm('Are you sure you want to delete this goal?')) {
        goals = goals.filter(g => g.id !== goalId);
        localStorage.setItem('financialGoals', JSON.stringify(goals));
        loadGoals();
    }
}

// Edit Goal
function editGoal(goalId) {
    const goal = goals.find(g => g.id === goalId);
    if (goal) {
        editingGoalId = goalId;
        document.getElementById('goalName').value = goal.name;
        document.getElementById('goalTarget').value = goal.target;
        document.getElementById('goalCurrent').value = goal.current;
        document.getElementById('goalDeadline').value = goal.deadline;
        document.getElementById('goalIcon').value = goal.icon;
        document.getElementById('goalFormTitle').textContent = 'Edit Goal';
        document.getElementById('goalSubmitBtn').textContent = 'Update Goal';
        toggleGoalModal();
    }
}

// Reset Goal Form
function resetGoalForm() {
    editingGoalId = null;
    document.getElementById('goalForm').reset();
    document.getElementById('goalFormTitle').textContent = 'Set New Goal';
    document.getElementById('goalSubmitBtn').textContent = 'Create Goal';
}

// Toggle Completed Goals
function toggleCompletedGoals() {
    const list = document.getElementById('completedGoalsList');
    if (list.style.display === 'none') {
        list.style.display = 'grid';
    } else {
        list.style.display = 'none';
    }
}

// ==================== HISTORY TAB ====================

// Load History Data
async function loadHistoryData() {
    try {
        const response = await fetch(`${API_BASE}/expenses`);
        const data = await response.json();
        const expenses = data.expenses || [];
        
        // Calculate historical data for last 6 months
        const historyData = calculateHistoricalData(expenses);
        
        // Update metrics
        updateHistoryMetrics(historyData);
        
        // Draw line chart
        drawHistoryLineChart(historyData);
        
        // Update top categories
        updateTopCategories(expenses);
        
        // Update monthly breakdown table
        updateHistoryTable(historyData);
        
    } catch (error) {
        console.error('Error loading history data:', error);
    }
}

// Calculate Historical Data for Last 6 Months
function calculateHistoricalData(expenses) {
    const today = new Date();
    const sixMonthsAgo = new Date(today.getFullYear(), today.getMonth() - 5, 1);
    
    const monthlyData = {};
    
    // Initialize 6 months
    for (let i = 0; i < 6; i++) {
        const date = new Date(today.getFullYear(), today.getMonth() - (5 - i), 1);
        const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
        const monthName = date.toLocaleDateString('en-US', { month: 'short' });
        
        monthlyData[key] = {
            month: monthName,
            year: date.getFullYear(),
            expenses: 0,
            income: 0,
            count: 0,
            categories: {}
        };
    }
    
    // Aggregate expense data
    expenses.forEach(expense => {
        const expenseDate = new Date(expense.date);
        if (expenseDate >= sixMonthsAgo) {
            const key = `${expenseDate.getFullYear()}-${String(expenseDate.getMonth() + 1).padStart(2, '0')}`;
            
            if (monthlyData[key]) {
                monthlyData[key].expenses += parseFloat(expense.amount);
                monthlyData[key].count += 1;
                
                // Track categories
                const category = expense.category || 'Uncategorized';
                monthlyData[key].categories[category] = (monthlyData[key].categories[category] || 0) + parseFloat(expense.amount);
            }
        }
    });
    
    return Object.values(monthlyData);
}

// Update History Metrics
function updateHistoryMetrics(historyData) {
    const totalExpenses = historyData.reduce((sum, month) => sum + month.expenses, 0);
    const monthsWithData = historyData.filter(m => m.expenses > 0).length;
    const avgMonthly = monthsWithData > 0 ? totalExpenses / monthsWithData : 0;
    
    const highestMonth = historyData.reduce((max, month) => 
        month.expenses > max.expenses ? month : max, historyData[0]);
    
    // Assuming income for demo (can be extended with actual income data)
    const estimatedIncome = totalExpenses * 1.3; // 30% more than expenses
    const totalSaved = estimatedIncome - totalExpenses;
    
    document.getElementById('avgMonthlySpend').textContent = `$${avgMonthly.toFixed(2)}`;
    document.getElementById('highestExpenseMonth').textContent = `$${highestMonth.expenses.toFixed(2)}`;
    document.getElementById('totalSaved').textContent = `$${totalSaved.toFixed(2)}`;
}

// Draw History Line Chart
function drawHistoryLineChart(historyData) {
    const canvas = document.getElementById('historyLineChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Chart settings
    const padding = { top: 40, right: 40, bottom: 60, left: 60 };
    const chartWidth = width - padding.left - padding.right;
    const chartHeight = height - padding.top - padding.bottom;
    
    // Find max value for scaling
    const maxExpense = Math.max(...historyData.map(d => d.expenses));
    const maxIncome = maxExpense * 1.3; // Income assumed higher
    const maxValue = Math.max(maxExpense, maxIncome);
    const yScale = chartHeight / maxValue;
    const xStep = chartWidth / (historyData.length - 1);
    
    // Draw grid lines
    ctx.strokeStyle = '#e0e0e0';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 5; i++) {
        const y = padding.top + (chartHeight / 5) * i;
        ctx.beginPath();
        ctx.moveTo(padding.left, y);
        ctx.lineTo(width - padding.right, y);
        ctx.stroke();
    }
    
    // Draw axes
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(padding.left, padding.top);
    ctx.lineTo(padding.left, height - padding.bottom);
    ctx.lineTo(width - padding.right, height - padding.bottom);
    ctx.stroke();
    
    // Draw expense line (red)
    ctx.strokeStyle = '#ef4444';
    ctx.lineWidth = 3;
    ctx.beginPath();
    historyData.forEach((data, i) => {
        const x = padding.left + xStep * i;
        const y = height - padding.bottom - (data.expenses * yScale);
        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    ctx.stroke();
    
    // Draw income line (green)
    ctx.strokeStyle = '#10b981';
    ctx.lineWidth = 3;
    ctx.beginPath();
    historyData.forEach((data, i) => {
        const income = data.expenses * 1.3; // Assumed income
        const x = padding.left + xStep * i;
        const y = height - padding.bottom - (income * yScale);
        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    ctx.stroke();
    
    // Draw net flow line (navy)
    ctx.strokeStyle = '#1e40af';
    ctx.lineWidth = 3;
    ctx.beginPath();
    historyData.forEach((data, i) => {
        const netFlow = (data.expenses * 1.3) - data.expenses; // Income - Expenses
        const x = padding.left + xStep * i;
        const y = height - padding.bottom - (netFlow * yScale);
        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    ctx.stroke();
    
    // Draw labels
    ctx.fillStyle = '#666';
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';
    historyData.forEach((data, i) => {
        const x = padding.left + xStep * i;
        ctx.fillText(data.month, x, height - padding.bottom + 20);
    });
}

// Update Top Categories
function updateTopCategories(expenses) {
    const categoryTotals = {};
    
    expenses.forEach(expense => {
        const category = expense.category || 'Uncategorized';
        categoryTotals[category] = (categoryTotals[category] || 0) + parseFloat(expense.amount);
    });
    
    const sortedCategories = Object.entries(categoryTotals)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3);
    
    const total = sortedCategories.reduce((sum, [, amount]) => sum + amount, 0);
    
    const container = document.querySelector('.top-categories-list');
    if (container && sortedCategories.length > 0) {
        container.innerHTML = sortedCategories.map(([category, amount], index) => {
            const percentage = ((amount / total) * 100).toFixed(1);
            const colors = ['#ef4444', '#f87171', '#fca5a5'];
            return `
                <div class="category-bar-item">
                    <div class="category-info">
                        <span class="category-name">${category}</span>
                        <span class="category-percentage">${percentage}%</span>
                    </div>
                    <div class="category-bar" style="width: ${percentage}%; background: ${colors[index]};">
                        <span class="category-amount">$${amount.toFixed(2)}</span>
                    </div>
                </div>
            `;
        }).join('');
    }
}

// Update History Table
function updateHistoryTable(historyData) {
    const tbody = document.getElementById('historyTableBody');
    if (!tbody) return;
    
    if (historyData.length === 0 || historyData.every(m => m.expenses === 0)) {
        tbody.innerHTML = '<tr><td colspan="5" class="no-data">No historical data available</td></tr>';
        return;
    }
    
    tbody.innerHTML = historyData.map(month => {
        const income = month.expenses * 1.3; // Assumed income
        const netFlow = income - month.expenses;
        const topCategory = Object.entries(month.categories)
            .sort((a, b) => b[1] - a[1])[0];
        
        return `
            <tr>
                <td>${month.month} ${month.year}</td>
                <td class="positive">$${income.toFixed(2)}</td>
                <td class="negative">$${month.expenses.toFixed(2)}</td>
                <td class="${netFlow >= 0 ? 'positive' : 'negative'}">$${netFlow.toFixed(2)}</td>
                <td>${topCategory ? topCategory[0] : 'N/A'}</td>
            </tr>
        `;
    }).join('');
}

// Toggle History Details
function toggleHistoryDetails() {
    const content = document.getElementById('historyDetailsContent');
    const icon = document.querySelector('.expandable-header .expand-icon');
    
    if (content.style.display === 'none') {
        content.style.display = 'block';
        icon.textContent = '▲';
    } else {
        content.style.display = 'none';
        icon.textContent = '▼';
    }
}

// Export History Report
function exportHistoryReport() {
    alert('Export functionality would generate a PDF/CSV report with historical data');
    // This would typically trigger a download of a report file
}
