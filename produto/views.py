from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse, JsonResponse
from .models import Produto

class ListaProdutos(ListView):
    model = Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'

class DetalheProdutos(View):
    def get(self, *args, **kwargs):
        return HttpResponse('DetalheProdutos')

class AddtoCart(View):
    def post(self, request):
        produto_id = request.POST.get('produto_id')
        produto = get_object_or_404(Produto, id=produto_id)

        carrinho = request.session.get('carrinho', {})

        if produto_id in carrinho:
            carrinho[produto_id]['quantidade'] += 1
        else:
            carrinho[produto_id] = {
                'nome': produto.nome,
                'preco': produto.preco_marketing_promo if produto.preco_marketing_promo else produto.preco_marketing,
                'quantidade': 1,
                'imagem': produto.imagem.url if produto.imagem else ''
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

        return render(request, 'produto/cart.html', {'carrinho': carrinho, 'total': total})

class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')