from django.shortcuts import render, get_object_or_404, redirect
from marketapp.models import Supermercado, ProdutoSupermercado
from django.http.response import Http404
import marketapp.services.carrinho as carrinho_service
from marketapp.utils.autorizacao import apenas_cliente
from django.contrib.auth.decorators import login_required
import marketapp.repository.produto as produto_repository


def home(request):
    return render(request, 'home.html')


@apenas_cliente()
def ver_produtos_supermercado(request, nome):
    try:
        supermercado = Supermercado.objects.get(nome_url=nome)
    except Supermercado.DoesNotExist:
        raise Http404
    produtos = ProdutoSupermercado.objects.filter(supermercado=supermercado)
    return render(request,
                  'cliente/ver_produtos_supermercado.html',
                  {'produtos': produtos,
                   'supermercado': supermercado})


@apenas_cliente()
def adicionar_produto_carrinho(request, produto_id):
    produto = get_object_or_404(ProdutoSupermercado, id=produto_id)
    carrinho_service.adicionar_produto(request, produto)
    return redirect('marketapp.views.cliente.ver_carrinho')


@login_required
def ver_carrinho(request):
    carrinho = carrinho_service.get_carrinho_usuario(request.user)
    return render(request,
                  'cliente/carrinho.html',
                  {'carrinho': carrinho})


@login_required
def comparar_supermercados(request):
    if 'ids' in request.GET:
        try:
            supermercados = request.GET.getlist('ids')
            supermercado_1 = Supermercado.objects.get(id=int(supermercados[0]))
            supermercado_2 = Supermercado.objects.get(id=int(supermercados[1]))
        except (KeyError, Supermercado.DoesNotExist):
            supermercados = Supermercado.objects.all()
            supermercado_1 = supermercados[0]
            supermercado_2 = supermercados[1]
    else:
        supermercados = Supermercado.objects.all()
        supermercado_1 = supermercados[0]
        supermercado_2 = supermercados[1]
    produtos = produto_repository.get_produtos_que_estejam_em_dois_supermercados(supermercado_1, supermercado_2)
    return render(request,
                  'cliente/comparacao_supermercados.html',
                  {'produtos':produtos,
                   's1':supermercado_1,
                   's2':supermercado_2})
