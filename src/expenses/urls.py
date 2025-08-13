from django.urls import path
from .views import (
    ExpenseListView, ExpenseCreateView, 
    ExpenseUpdateView, ExpenseDeleteView,
    CategoryListView, CategoryCreateView, 
    CategoryDeleteView, ExpenseSummaryView,
    ReminderListView, ReminderCreateView,
    ReminderUpdateView, ReminderDeleteView,
    BudgetListView, BudgetCreateView,
    BudgetUpdateView, BudgetDeleteView,
    expense_summary_json
)

app_name = 'expenses'
urlpatterns = [
    path('', ExpenseListView.as_view(), name='list'),
    path('create/', ExpenseCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', ExpenseUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', ExpenseDeleteView.as_view(), name='delete'),
    
     # Category URLs
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    
    path('summary/', ExpenseSummaryView.as_view(), name='summary'),
    path('summary/json/', expense_summary_json, name='summary_json'),
    
    # Reminder URLs
    path('reminders/', ReminderListView.as_view(), name='reminder_list'),
    path('reminders/create/', ReminderCreateView.as_view(), name='reminder_create'),
    path('reminders/<int:pk>/edit/', ReminderUpdateView.as_view(), name='reminder_edit'),
    path('reminders/<int:pk>/delete/', ReminderDeleteView.as_view(), name='reminder_delete'),
    
    # Budget URLs
    path('budgets/', BudgetListView.as_view(), name='budget_list'),
    path('budgets/create/', BudgetCreateView.as_view(), name='budget_create'),
    path('budgets/<int:pk>/edit/', BudgetUpdateView.as_view(), name='budget_edit'),
    path('budgets/<int:pk>/delete/', BudgetDeleteView.as_view(), name='budget_delete'),
]