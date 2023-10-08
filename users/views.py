from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login


def register(request):
    if request.method == "GET":
        return render(request, 'register.html')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not password == confirm_password:
            messages.add_message(request, constants.ERROR,
                                 'As senhas não são iguais')
            return redirect('/users/register')

        if len(password) < 6:
            messages.add_message(request, constants.ERROR,
                                 'A precisa ter mais que 6 caracteres')
            return redirect('/users/register')

        if User.objects.filter(username=username).exists():
            messages.add_message(request, constants.ERROR,
                                 'Nome do usuário já existe. Escolha outro!')
            return redirect('/users/register')

        try:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            messages.add_message(request, constants.SUCCESS,
                                 f'Login criado para o e-mail{user.email}')

        except Exception:
            messages.add_message(request, constants.ERROR,
                                 'Erro ao cadastrar, contate um administrador')
            return redirect('/users/register')

        return redirect('/users/register')


def Login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            # Acontecerá um erro ao redirecionar por enquanto,
            # resolveremos nos próximos passos
            return redirect('/')
        else:
            messages.add_message(request, constants.ERROR,
                                 'Usuario ou senha inválidos')
            return redirect('/users/login')
