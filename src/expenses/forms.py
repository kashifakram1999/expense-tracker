from django import forms
from .models import Expense, Category, Budget

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'description', 'payment_method']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'is_default']
        
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        
    def clean_name(self):
        name = self.cleaned_data['name']
        if Category.objects.filter(user=self.user, name__iexact=name).exists():
            raise forms.ValidationError("You already have a category with this name.")
        return name
    

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'period', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)
        self.fields['category'].required = False