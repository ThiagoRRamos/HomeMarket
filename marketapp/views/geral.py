from django.shortcuts import render, get_object_or_404
from marketapp.models import Supermercado, Produto, ProdutoSupermercado,PromocaoCombinacao


def home(request):
    supermercados = Supermercado.objects.all()
    return render(request, 'home.html', {'supermercados': supermercados})


def ver_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    produtos_supermercados = ProdutoSupermercado.objects.filter(produto=produto)
    return render(request,
                  'ver_produto.html',
                  {'produto': produto,
                   'pss': produtos_supermercados})

def ver_promocao(request, promocaoCombinacao_id):
    promocao = get_object_or_404(PromocaoCombinacao, id=promocaoCombinacao_id)
    return render(request,
                  'ver_promocao.html',
                  {'promocao': promocao})