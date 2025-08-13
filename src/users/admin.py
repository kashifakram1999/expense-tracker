from django.contrib import admin
from .models import User, Profile

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')
    ordering = ('-id',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ['user__username']
    list_filter = ('user',)
    ordering = ('-id',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user) if not request.user.is_superuser else qs
