def cart_item_count(request):
    carrinho = request.session.get('carrinho', {})
    item_count = len(carrinho)
    return {'cart_item_count': item_count}