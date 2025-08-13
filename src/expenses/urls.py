from django.urls import path
from .views import (
    ExpenseListView, ExpenseCreateView, 
    ExpenseUpdateView, ExpenseDeleteView,
    CategoryListView, CategoryCreateView, 
    CategoryDeleteView,
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
]