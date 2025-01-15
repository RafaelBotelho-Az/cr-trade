from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse
from .forms import RegisterForm


def createUser(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            print('Registrado com sucesso!')
            return redirect('produto:lista')
    else:
        form = RegisterForm()


    return render(
        request,
        'perfil/create-user.html',
        {
            'form': form,
            'title': 'Cadastro',
        }
    )

def loginView(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print('Logado com sucesso!')
            return redirect('produto:lista')
        else:
            messages.error(request, 'Usuário ou senha inválidos!')
            print('Login inválido!')
            return redirect(f"{reverse('produto:lista')}?login_error=true")

    return redirect('produto:lista')