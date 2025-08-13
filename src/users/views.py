from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordResetView,LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import SignUpForm, ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from .models import Profile

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create profile for new user
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('expenses:list')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    return LoginView.as_view(
        template_name='users/login.html',
        redirect_authenticated_user=True,
        success_url=reverse_lazy('expenses:list')
    )(request)

def logout_view(request):
    logout(request)
    return redirect('users:login')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('expenses:list')
    
    def get_object(self):
        # Get or create profile if it doesn't exist
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile