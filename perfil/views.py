from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages, auth
from allauth.account.views import LoginView
from .forms import RegisterForm
from django.urls import reverse
from produto.models import Categoria
from pedido.models import Pedido


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


@login_required(login_url='/')
def meus_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).select_related('usuario').prefetch_related('itens').order_by('-criado_em')

    return render(request, 'perfil/meus-pedidos.html', {'pedidos': pedidos})

@login_required
def cancelar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)

    if pedido.status in ['P', 'C']:
        pedido.delete()
        messages.success(request, "Pedido Cancelado com sucesso.")
    else:
        messages.error(request, "Este pedido não pode ser Cancelado.")

    return redirect('perfil:meus_pedidos')