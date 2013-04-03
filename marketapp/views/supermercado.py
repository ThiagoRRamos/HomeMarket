from django.shortcuts import render, redirect
from marketapp.models import Produto
from django.forms.models import ModelForm
from marketapp.forms import ProdutoForm, ProdutoSupermercadoForm


def home(request):
    return render(request, 'home.html')


def adicionar_produto(request):
    if request.method == 'POST':
        codigo = request.POST['codigo']
        try:
            produto = Produto.objects.get(codigo_de_barras=codigo)
            produto.nome = "nome"
            produto.save()
            return redirect('/adicionar-produto-existente/' + codigo)
        except Produto.DoesNotExist:
            return redirect('/criar_produto')
    return render(request, 'inicio_adicao.html')


def criar_produto(request):
    form = ProdutoForm()
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return render(request, 'criacao_produto.html',
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
    return render(request, 'adicao_produto.html',
                  {'form': form})