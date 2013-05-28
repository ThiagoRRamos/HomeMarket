from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import inlineformset_factory

from marketapp.models import Produto, ProdutoSupermercado, RegiaoAtendida, \
    Supermercado, Compra
from marketapp.forms import ProdutoForm, ProdutoSupermercadoForm, \
    ProdutoSupermercadoFormPreco
from marketapp.utils.autorizacao import apenas_supermercado, apenas_cliente
import marketapp.repository.produto as produto_repository
from django import forms
from marketapp import services
from marketapp.services import supermercado


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


@apenas_supermercado
def criar_produto(request):
    form = ProdutoForm()
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save()
            return redirect('marketapp.views.supermercado.adicionar_produto_existente',
                            codigo=produto.codigo_de_barras)
    return render(request, 'supermercado/criacao_produto.html',
                  {'form': form})
@apenas_cliente
def avaliar_supermercado(request,id_supermercado):   
    if request.method == 'POST':
        nota = request.POST['nota']
        avaliacao = request.POST['avaliacao']
        services.supermercado.gerar_avaliacao_supermercado(nota, avaliacao, id_supermercado,request.user.consumidor)
    return render(request, 'supermercado/avaliacao_supermercado.html')

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
    produtos = ProdutoSupermercado.objects.filter(supermercado=request.user.supermercado)
    return render(request,
                  'supermercado/modificar_preco.html',
                  {'produtos': produtos})


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
    produtos = ProdutoSupermercado.objects.filter(supermercado=request.user.supermercado)
    if 'codigo' in request.GET:
        codigo = request.GET['codigo']
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
                  'supermercado/inicio_comparacao.html',
                  {'produtos': produtos})


@apenas_supermercado
def definir_regiao_atendida(request):
    CFormset = inlineformset_factory(Supermercado, RegiaoAtendida)

    if request.method == 'POST':
        formset = CFormset(request.POST, instance=request.user.supermercado)
        if formset.is_valid():
            formset.save()
    else:
        formset = CFormset(instance=request.user.supermercado)
    for form in formset.forms:
            form.fields['preco'].widget = forms.TextInput(attrs={'class':'input-small'})
            form.fields['tempo'].widget = forms.TextInput(attrs={'class':'input-small'})
    return render(request,
                    'supermercado/definir_regiao.html',
                    {'formset': formset})


@apenas_supermercado
def status_compras(request):
    compras = Compra.objects.filter(supermercado=request.user.supermercado)
    return render(request,
                  'supermercado/status_compras.html',
                  {'compras': compras})


@apenas_supermercado
def atualizar_status(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id,
                               supermercado=request.user.supermercado)
    compra.status_pagamento = request.GET['status']
    compra.save()
    return redirect('/status-compras')
