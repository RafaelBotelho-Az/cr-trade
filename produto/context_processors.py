from allauth.account.forms import LoginForm
from produto.models import Categoria

def cart_item_count(request):
    carrinho = request.session.get('carrinho', {})
    item_count = len(carrinho)
    return {'cart_item_count': item_count}


def allauth_forms(request):
    return {
        'allauth_login_form': LoginForm(),
    }

def jogo_categoria(request):
    jogos = Categoria.objects.all()
    return {'jogos': jogos}