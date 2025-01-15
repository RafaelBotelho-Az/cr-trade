from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
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