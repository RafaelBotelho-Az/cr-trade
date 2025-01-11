from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse

class ListaProdutos(View):
    def get(self, *args, **kwargs):
        return HttpResponse('ListaProdutos')

class DetalheProdutos(View):
    def get(self, *args, **kwargs):
        return HttpResponse('DetalheProdutos')

class AddtoCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('AddtoCart')
    
class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('RemoveFromCart')

class Cart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Cart')

class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')