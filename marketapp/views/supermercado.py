from django import forms
from django.db.models import Count
from django.db.models.aggregates import Sum
from django.forms.models import inlineformset_factory, ModelForm
from django.shortcuts import render, redirect, get_object_or_404
import marketapp.services.supermercado as supermercado_service
from marketapp.forms import ProdutoForm, ProdutoSupermercadoForm, \
    ProdutoSupermercadoFormPreco
from marketapp.models import Produto, ProdutoSupermercado, RegiaoAtendida, \
    Supermercado, Compra, PromocaoCombinacao, CompraAgendada, CompraRecorrente, \
    ProdutoCompra
from marketapp.services.analisador_promocoes import promocoes_supermercado
from marketapp.utils.autorizacao import apenas_supermercado, apenas_cliente
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
def avaliar_supermercado(request, id_supermercado):   
    if request.method == 'POST':
        nota = request.POST['nota']
        avaliacao = request.POST['avaliacao']
        supermercado_service.gerar_avaliacao_supermercado(nota, avaliacao, id_supermercado, request.user.consumidor)
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


@apenas_supermercado
def compras_recorrentes(request):
    recorrentes = CompraRecorrente.objects.filter(supermercado=request.user.supermercado)
    return render(request,
                  'supermercado/compras_recorrentes.html',
                  {'compras_recorrentes': recorrentes})


@apenas_supermercado
def compras_agendadas(request):
    agendadas = CompraAgendada.objects.filter(supermercado=request.user.supermercado)
    return render(request,
                  'supermercado/compras_agendadas.html',
                  {'compras_agendadas': agendadas})


@apenas_supermercado
def gerenciar_promocoes(request):
    promocoes = promocoes_supermercado(request.user.supermercado)
    return render(request,
                  'supermercado/gerenciar_promocoes.html',
                  {'promocoes': promocoes})


@apenas_supermercado
def adicionar_promocoes(request):
    class Promo(ModelForm):
        class Meta:
            model = PromocaoCombinacao
            exclude = ['supermercado']
    if request.method == 'POST':
        form = Promo(request.POST)
        if form.is_valid():
            pro = form.save(commit=False)
            pro.supermercado = request.user.supermercado
            pro.save()
            form.save_m2m()
    else:
        form = Promo()
        form.fields['produtos'].queryset = ProdutoSupermercado.objects.filter(supermercado=request.user.supermercado)
    return render(request,
                  'supermercado/adicao_promocao.html',
                  {'form': form})


@apenas_supermercado
def ver_historico_vendas(request):
    vendas = Compra.objects.filter(supermercado=request.user.supermercado)
    produtos_vendidos = ProdutoCompra.objects.filter(compra__supermercado=request.user.supermercado).values('produto__produto__nome').annotate(quantidade_total=Sum('quantidade'))
    return render(request,
                  'supermercado/historico_vendas.html',
                  {'vendas': vendas,
                   'produtos': produtos_vendidos})


@apenas_supermercado
def ver_promocao(request, promocao_id):
    promocao = PromocaoCombinacao.objects.get(id=promocao_id)
    return render(request,
                  'supermercado/ver_promocao.html',
                  {'promocao': promocao})


@apenas_supermercado
def apagar_promocao(request, promocao_id):
    PromocaoCombinacao.objects.filter(id=promocao_id).delete()
    return redirect('/promocoes')