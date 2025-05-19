from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def tambah_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # ganti dengan nama url dashboard Anda
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/tambah_user.html', {'form': form})

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('admin_dashboard')  # pastikan nama url-nya sesuai di urls.py
            else:
                error = "Akun Anda tidak aktif. Hubungi admin."
        else:
            error = "Username atau password salah."
    return render(request, 'users/login.html', {'error': error})