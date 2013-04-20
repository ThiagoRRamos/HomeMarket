from django.shortcuts import render, redirect

from marketapp.models import Produto, ProdutoSupermercado
from marketapp.forms import ProdutoForm, ProdutoSupermercadoForm, \
    ProdutoSupermercadoFormPreco
from marketapp.utils.autorizacao import apenas_supermercado
import marketapp.repository.produto as produto_repository


@apenas_supermercado
def home(request):
    supermercado_atual = request.user.supermercado
    return render(request,
                  'supermercado/home.html',
                  {'nome': supermercado_atual})


@apenas_supermercado
def adicionar_produto(request):
    if request.method == 'POST':
        codigo = request.POST['codigo']
        try:
            Produto.objects.get(codigo_de_barras=codigo)
            return redirect('/adicionar-produto-existente/' + codigo)
        except Produto.DoesNotExist:
            return redirect('/criar_produto')
    return render(request, 'supermercado/inicio_adicao.html')


def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save()
            return redirect('marketapp.views.supermercado.adicionar_produto_existente',
                            codigo=produto.codigo_de_barras)
    return render(request, 'supermercado/criacao_produto.html',
                  {'form': form})


def adicionar_produto_existente(request, codigo):
    form = ProdutoSupermercadoForm()
    if request.method == 'POST':
        form = ProdutoSupermercadoForm(request.POST)
        if form.is_valid():
            prod = form.save(commit=False)
            prod.supermercado = request.user.supermercado
            prod.produto = Produto.objects.get(codigo_de_barras=codigo)
            prod.save()
    return render(request,
                  'supermercado/adicao_produto.html',
                  {'form': form})


@apenas_supermercado
def modificar_preco(request):
    if request.method == 'POST':
        codigo = request.POST['codigo']
        try:
            produto = Produto.objects.get(codigo_de_barras=codigo)
            produto.save()
            return redirect('/modificar-preco-existente/' + codigo)
        except Produto.DoesNotExist:
            return redirect('/criar_produto')
    return render(request, 'supermercado/modificar_preco.html')


@apenas_supermercado
def modificar_preco_existente(request, codigo):
    produto_supermercado = ProdutoSupermercado.objects.get(produto=Produto.objects.get(codigo_de_barras=codigo),
                                                           supermercado=request.user.supermercado)
    form = ProdutoSupermercadoFormPreco(instance=produto_supermercado)
    if request.method == 'POST':
        form = ProdutoSupermercadoFormPreco(request.POST, instance=produto_supermercado)
        if form.is_valid():
            prod = form.save(commit=False)
            prod.supermercado = request.user.supermercado
            prod.produto = Produto.objects.get(codigo_de_barras=codigo)
            prod.save()
    return render(request,
                  'supermercado/modificacao_preco.html',
                  {'form': form})


@apenas_supermercado
def comparar_produto_preco(request):
    if request.method == 'POST':
        codigo = request.POST['codigo']
        try:
            produto = Produto.objects.get(codigo_de_barras=codigo)
            supermercados = produto_repository.get_supermercados_produto(produto)
            return render(request,
                          'cliente/comparar_precos.html',
                          {'sp': supermercados,
                           'produto': produto})
        except Produto.DoesNotExist:
            return redirect('/criar_produto')
    return render(request,
                  'supermercado/inicio_comparacao.html')
