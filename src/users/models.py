from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    # Add custom fields
    currency = models.CharField(_('Currency'), max_length=3, default='USD')
    timezone = models.CharField(_('Timezone'), max_length=50, default='UTC')
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    monthly_budget = models.DecimalField(
        _('Monthly Budget'), 
        max_digits=10, 
        decimal_places=2, 
        default=0.00
    )
    default_category = models.ForeignKey(
        'expenses.Category', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    def __str__(self):
        return f"{self.user.username}'s Profile"