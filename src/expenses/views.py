from random import randint
from django.views.generic import ListView, CreateView, UpdateView, DeleteView ,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.urls import reverse_lazy
from .models import Expense, Category, Budget, Reminder
from .forms import ExpenseForm, CategoryForm, BudgetForm
from django.db.models import Sum
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils import timezone

class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'
    
    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expenses:list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.currency = self.request.user.currency
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expenses:list')
    
    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'expenses/expense_confirm_delete.html'
    success_url = reverse_lazy('expenses:list')
    
    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

class ExpenseSummaryView(LoginRequiredMixin, TemplateView):
    template_name = 'expenses/summary.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Default to last 30 days
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
        
        # Get expenses grouped by category
        expenses = Expense.objects.filter(
            user=self.request.user,
            date__range=[start_date, end_date]
        ).values('category__name').annotate(total=Sum('amount'))
        
        context['summary_data'] = list(expenses)
        context['start_date'] = start_date
        context['end_date'] = end_date
        return context

def expense_summary_json(request):
    """JSON endpoint for expense summary data"""
    # Get date range from request
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    
    if not start_date or not end_date:
        # Default to last 30 days
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    # Get expenses grouped by category
    expenses = Expense.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    ).values('category__name').annotate(total=Sum('amount'))
    
    # Format data for Chart.js
    labels = []
    data = []
    background_colors = []
    
    for item in expenses:
        labels.append(item['category__name'] or 'Uncategorized')
        data.append(float(item['total']))
        background_colors.append(f'rgba({randint(0, 255)}, {randint(0, 255)}, {randint(0, 255)}, 0.6)')
    
    return JsonResponse({
        'labels': labels,
        'datasets': [{
            'label': 'Expenses by Category',
            'data': data,
            'backgroundColor': background_colors,
        }]
    })

# Similar views for Category (CreateView, ListView, DeleteView)
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'expenses/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'expenses/category_form.html'
    success_url = reverse_lazy('expenses:category_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'expenses/category_confirm_delete.html'
    success_url = reverse_lazy('expenses:category_list')
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    

class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'expenses/budget_list.html'
    context_object_name = 'budgets'
    
    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'expenses/budget_form.html'
    success_url = reverse_lazy('expenses:budget_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'expenses/budget_form.html'
    success_url = reverse_lazy('expenses:budget_list')
    
    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    template_name = 'expenses/budget_confirm_delete.html'
    success_url = reverse_lazy('expenses:budget_list')
    
    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
    
# Reminder views
class ReminderListView(LoginRequiredMixin, ListView):
    model = Reminder
    template_name = 'expenses/reminder_list.html'
    context_object_name = 'reminders'
    
    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user)

class ReminderCreateView(LoginRequiredMixin, CreateView):
    model = Reminder
    fields = ['title', 'message', 'due_date']
    template_name = 'expenses/reminder_form.html'
    success_url = reverse_lazy('expenses:reminder_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ReminderUpdateView(LoginRequiredMixin, UpdateView):
    model = Reminder
    fields = ['title', 'message', 'due_date', 'email_sent']
    template_name = 'expenses/reminder_form.html'
    success_url = reverse_lazy('expenses:reminder_list')
    
    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user)

class ReminderDeleteView(LoginRequiredMixin, DeleteView):
    model = Reminder
    template_name = 'expenses/reminder_confirm_delete.html'
    success_url = reverse_lazy('expenses:reminder_list')
    
    def get_queryset(self):
        return Reminder.objects.filter(user=self.request.user)