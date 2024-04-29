from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .models import User
from .forms import LoginForm, RegisterForm


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('aurora')
        user = User
        form = LoginForm()
        return render(request, 'user_form.html', {'user': user, 'form': form})

    def post(self, request):
        form = LoginForm()
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user_name = request.POST.get('user_name')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            user = None

            try:
                user = User.objects.get(email=email)
            except Exception as e:
                print(e)
                messages.error(request, 'User does not exist')
                return render(request, 'user_form.html', {'user': user, 'form': form})

            user = authenticate(request, email=user, password=password, last_name=last_name, first_name=first_name,
                                user_name=user_name)
            if user is not None:
                login(request, user)
                return redirect('aurora')
            else:
                messages.error(request, 'User was not found')

        return render(request, 'user_form.html')


class RegisterView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            form = RegisterForm()
            return render(request, 'user_form.html', {'form': form})
        else:
            return redirect('aurora')

    def post(self, request):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            # do some cleaning
            user.save()
            login(request, user)
            return redirect('aurora')
        else:
            messages.error(request, 'An errors occurred during registration')

        return render(request, 'user_form.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            logout(request)
            return redirect('aurora')


class UpdateUserView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = RegisterForm(instance=request.user)
            if form.is_valid():
                user = form.save(commit=False)
                # do some cleaning
                user.save()
                login(request, user)
                return redirect('aurora')
            else:
                messages.error(request, 'Failed to update user')
        else:
            return redirect('login')
        return render(request, 'user_form.html', {'form': form})
