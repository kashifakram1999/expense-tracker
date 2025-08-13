from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='categories'
    )
    name = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ('user', 'name')
    
    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    date = models.DateField()
    description = models.TextField(blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'category']),
        ]
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.amount} {self.currency} - {self.category}"