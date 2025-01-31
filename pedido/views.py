from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.http import JsonResponse
from .models import Pedido, ItemPedido
from produto.models import Categoria


def criar_pedido(request):

    if not request.user.is_authenticated:
        messages.warning(request, "Você precisa estar logado para criar um pedido.")
        return redirect('produto:cart')

    carrinho = request.session.get('carrinho', {})
    if not carrinho:
        messages.error(request, "Seu carrinho está vazio.")
        return redirect('produto:lista')

    numero_pedido = get_random_string(12).upper()
    pedido = Pedido.objects.create(
        usuario=request.user,
        numero=numero_pedido,
        total=0
    )

    total_pedido = 0
    for produto_id, item in carrinho.items():
        preco = item['preco']
        quantidade = item['quantidade']
        total_item = preco * quantidade
        total_pedido += total_item

        ItemPedido.objects.create(
            pedido=pedido,
            produto_id=produto_id,
            preco=preco,
            quantidade=quantidade,
            imagem=item['imagem'],
        )

    pedido.total = total_pedido
    pedido.save()
    del request.session['carrinho']

    return redirect('pedido:detalhe', pk=pedido.pk)


@login_required
def detalhe_pedido(request, pk):
    try:
        pedido = Pedido.objects.get(pk=pk, usuario=request.user)
    except Pedido.DoesNotExist:
        messages.error(request, "Você não tem permissão para acessar este pedido.")
        return redirect('produto:lista')

    if request.method == 'POST':
        forma_pagamento = request.POST.get('forma_pagamento')
        in_game_name = request.POST.get('in_game_name', '').strip()

        if not forma_pagamento:
            messages.error(request, "Por favor, selecione uma forma de pagamento.")
            return redirect('pedido:detalhe', pk=pedido.pk)

        if in_game_name:
            pedido.in_game_name = in_game_name
            pedido.save()
            messages.success(request, "Success!")
        else:
            messages.error(request, "O nome in-game não pode estar vazio.")
            return redirect('pedido:detalhe', pk=pedido.pk)
        
    Jogos = Categoria.objects.all()

    return render(request, 'pedido/detalhe.html', {'pedido': pedido, 'jogos': Jogos})