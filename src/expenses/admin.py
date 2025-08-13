from django.contrib import admin
from .models import Expense, Category, Budget , Reminder

# Register your models here.
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category', 'amount', 'currency', 'date', 'created_at')
    search_fields = ('user__username', 'category__name', 'amount')
    list_filter = ('user', 'category', 'date')
    ordering = ('-date',)
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'is_default')
    search_fields = ('user__username', 'name')
    list_filter = ('user', 'is_default')
    ordering = ('name',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user) if not request.user.is_superuser else qs
    
@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'category', 'amount', 'period', 'start_date', 'end_date')
    search_fields = ('user__username', 'category__name', 'amount')
    list_filter = ('user', 'category', 'period')
    ordering = ('-start_date',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user) if not request.user.is_superuser else qs
    
@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at')
    search_fields = ('user__username', 'title')
    list_filter = ['user']
