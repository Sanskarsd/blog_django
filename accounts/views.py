from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import ProfileForm, RegisterForm, UserForm

def register(request):
    if request.user.is_authenticated: return redirect('blog:dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(); login(request, user); messages.success(request, 'Welcome to Inkstone!')
        return redirect('blog:dashboard')
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    user_form = UserForm(request.POST or None, instance=request.user)
    profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
    if request.method == 'POST' and user_form.is_valid() and profile_form.is_valid():
        user_form.save(); profile_form.save(); messages.success(request, 'Your profile has been updated.')
        return redirect('accounts:profile')
    return render(request, 'accounts/profile.html', {'user_form': user_form, 'profile_form': profile_form})
