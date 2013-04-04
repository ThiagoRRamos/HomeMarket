from django.shortcuts import render
from marketapp.models import Supermercado, ProdutoSupermercado
from django.http.response import Http404


def home(request):
    return render(request, 'home.html')


def ver_produtos_supermercado(request, nome):
    try:
        supermercado = Supermercado.objects.get(nome_url=nome)
    except Supermercado.DoesNotExist:
        raise Http404
    produtos = ProdutoSupermercado.objects.filter(supermercado=supermercado)
    return render(request,
                  'ver_produtos_supermercado.html',
                  {'produtos': produtos,
                   'supermercado':supermercado})