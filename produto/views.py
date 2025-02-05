from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic.list import ListView
from django.views import View
from django.http import JsonResponse
from .models import Produto, Categoria


def index(request):
    jogos = Categoria.objects.all()
    form = AuthenticationForm()

    context = {
        'jogos': jogos,
        'loginForm': form
        }

    return render(
            request,
            'produto/index.html',
            context
        )


class ListaProdutos(ListView):
    model = Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'

    def get_queryset(self):
        categoria_id = self.kwargs.get('jogo_id')
        tipo = self.kwargs.get('tipo')
        queryset = Produto.objects.filter(categoria_id=categoria_id)

        if tipo == 'moedas':
            queryset = queryset.filter(tipo='tipo1')
        elif tipo == 'servicos':
            queryset = queryset.filter(tipo='tipo2')
        elif tipo == 'gold':
            queryset = queryset.filter(tipo='tipo3')
        elif tipo == 'outros':
            queryset = queryset.filter(tipo='tipo4')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loginForm'] = AuthenticationForm()
        context['categoria'] = get_object_or_404(Categoria, id=self.kwargs.get('jogo_id'))
        context['jogos'] = Categoria.objects.all()
        
        tipo_escolhido = self.kwargs.get('tipo')

        if tipo_escolhido:
            context['tipo_selecionado'] = tipo_escolhido
        else:
            context['tipo_selecionado'] = 'Tudo'

        return context

class AddtoCart(View):
    def post(self, request):
        produto_id = request.POST.get('produto_id')
        produto = get_object_or_404(Produto, id=produto_id)
        carrinho = request.session.get('carrinho', {})

        if carrinho:
            primeira_categoria_id = list(carrinho.values())[0].get('categoria_id')

            if produto.categoria.id != primeira_categoria_id:
                messages.error(request, "Você só pode adicionar produtos da mesma categoria ao carrinho.")
                return redirect('produto:cart')

        if produto_id in carrinho:
            carrinho[produto_id]['quantidade'] += 1
        else:
            carrinho[produto_id] = {
                'nome': produto.nome,
                'preco': produto.preco_marketing_promo if produto.preco_marketing_promo else produto.preco_marketing,
                'quantidade': 1,
                'imagem': produto.imagem.url if produto.imagem else '',
                'categoria_id': produto.categoria.id
            }

        request.session['carrinho'] = carrinho
        return redirect('produto:cart')
    
class RemoveFromCart(View):
    def post(self, request):
        produto_id = request.POST.get('produto_id')

        carrinho = request.session.get('carrinho', {})
        if produto_id in carrinho:
            del carrinho[produto_id]

        request.session['carrinho'] = carrinho
        return redirect('produto:cart')
    

class UpdateCart(View):
    def post(self, request):
        produto_id = request.POST.get('produto_id')
        acao = request.POST.get('acao')

        carrinho = request.session.get('carrinho', {})

        if produto_id in carrinho:
            if acao == 'incrementar':
                carrinho[produto_id]['quantidade'] += 1
            elif acao == 'decrementar' and carrinho[produto_id]['quantidade'] > 1:
                carrinho[produto_id]['quantidade'] -= 1

            request.session['carrinho'] = carrinho

            subtotal = carrinho[produto_id]['quantidade'] * carrinho[produto_id]['preco']
            total = sum(item['preco'] * item['quantidade'] for item in carrinho.values())

            return JsonResponse({
                'quantidade': carrinho[produto_id]['quantidade'],
                'subtotal': subtotal,
                'total': total
            })
        else:
            return JsonResponse({'error': 'Produto não encontrado'}, status=400)

class Cart(View):
    def get(self, request):
        carrinho = request.session.get('carrinho', {})
        total = sum(item['preco'] * item['quantidade'] for item in carrinho.values())

        for produto_id, item in carrinho.items():
            item['subtotal'] = item['preco'] * item['quantidade']

        ultima_categoria_id = None
        if carrinho:
            ultima_categoria_id = list(carrinho.values())[-1].get('categoria_id', None)

        form = AuthenticationForm()
        jogos = Categoria.objects.all()
        return render(
            request, 
                'produto/cart.html', {
                'carrinho': carrinho, 
                'total': total, 
                'loginForm': form, 
                'ultima_categoria_id': ultima_categoria_id,
                'jogos': jogos
                }
        )
