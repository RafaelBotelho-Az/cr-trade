from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages, auth
from allauth.account.views import LoginView
from .forms import RegisterForm
from produto.models import Categoria
from django.urls import reverse


class MyLoginView(LoginView):
    def form_invalid(self, form):
        messages.error(self.request, "Usuário ou senha inválidos!")

        url_com_param = reverse('produto:index') + '?login_error=true'
        return redirect(url_com_param)

def createUser(request):
    loginForm = AuthenticationForm(prefix='register')
    jogos = Categoria.objects.all()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado com sucesso!')
            return redirect('produto:index')
    else:
        form = RegisterForm()


    return render(
        request,
        'perfil/create-user.html',
        {
            'form': form,
            'loginForm': loginForm,
            'jogos': jogos,
        }
    )

def logoutView(request):
    auth.logout(request)
    return redirect('produto:index')