from django.shortcuts import render, redirect
from marketapp.models import Produto
<<<<<<< HEAD
from django.forms.models import ModelForm
from marketapp.forms import ProdutoForm, ProdutoSupermercadoForm, ProdutoSupermercadoFormPreco
from marketapp.autorizacao import apenas_supermercado, apenas_cliente
=======
from marketapp.forms import ProdutoForm, ProdutoSupermercadoForm
from marketapp.autorizacao import apenas_supermercado
>>>>>>> 83490397e058207db973ec206c9b3c6b1a35e100


def home(request):
    return render(request, 'home.html')

@apenas_supermercado()
def funcionalidades_supermercado(request):
    nome = request.user.supermercado
    return render(request, 'supermercado_funcionalidades.html',{'nome' :nome})



@apenas_supermercado
def adicionar_produto(request):
    if request.method == 'POST':
        codigo = request.POST['codigo']
        try:
            produto = Produto.objects.get(codigo_de_barras=codigo)
            return redirect('/adicionar-produto-existente/' + codigo)
        except Produto.DoesNotExist:
            return redirect('/criar_produto')
    return render(request, 'inicio_adicao.html')

@apenas_supermercado()
def modificar_preco(request):
    if request.method == 'POST':
        codigo = request.POST['codigo']
        try:
            produto = Produto.objects.get(codigo_de_barras=codigo)
            produto.nome = "nome"
            produto.save()
            return redirect('/modificar-preco-existente/' + codigo)
        except Produto.DoesNotExist:
            return redirect('/criar_produto')
    return render(request, 'modificar_preco.html')




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
<<<<<<< HEAD
    
def modificar_preco_existente(request, codigo):
    form = ProdutoSupermercadoFormPreco()
    if request.method == 'POST':
        form = ProdutoSupermercadoFormPreco(request.POST)
        if form.is_valid():
            prod = form.save(commit=False)
            prod.supermercado = request.user.supermercado
            prod.produto = Produto.objects.get(codigo_de_barras=codigo)
            prod.save()
    return render(request, 'modificacao_preco.html',
                  {'form': form})

        
    
=======
>>>>>>> 83490397e058207db973ec206c9b3c6b1a35e100
