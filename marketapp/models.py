from django.db import models
from django.contrib.auth.models import User
from django.template.context import Context
from django.template.loader import get_template


class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField()

    def __unicode__(self):
        return self.nome


class Produto(models.Model):
    UNIDADES = (('mL', 'mL'),
                ('L', 'L'),
                ('g', 'g'),
                ('un', 'un'),
                ('Kg', 'Kg'))
    imagem = models.ImageField(upload_to="produtos", default="examples/produto.jpg")
    nome = models.CharField(max_length=50)
    descricao = models.TextField()
    codigo_de_barras = models.CharField(max_length=15, unique=True)
    categoria = models.ForeignKey(Categoria)
    quantidade = models.IntegerField()
    quantidade_unidade = models.CharField(max_length=5,
                                          choices=UNIDADES)

    def __unicode__(self):
        return self.nome


class Consumidor(models.Model):

    class Meta:
        verbose_name_plural = u'Consumidores'

    usuario = models.OneToOneField(User)
    cpf = models.CharField(max_length=20)
    cep = models.CharField(max_length=10)

    def __unicode__(self):
        return self.usuario.username


class Supermercado(models.Model):
    usuario = models.OneToOneField(User)
    nome_exibicao = models.CharField(max_length=50)
    nome_url = models.SlugField()

    def __unicode__(self):
        return self.nome_exibicao

    def get_absolute_url(self):
        return '/supermercado/{}'.format(self.nome_url)


class RegiaoAtendida(models.Model):
    supermercado = models.ForeignKey(Supermercado)
    cep_inicio = models.CharField(max_length=10)
    cep_final = models.CharField(max_length=10)


class ListaCompras(models.Model):
    class Meta:
        verbose_name = u'Lista de Compras'
        verbose_name_plural = u'Listas de Compras'
    nome = models.CharField(max_length=50)
    consumidor = models.ForeignKey(Consumidor)
    produtos = models.ManyToManyField(Produto, through='ProdutoLista')
    data_criacao = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return "Lista '{}' de {} de {}".format(self.nome,
                                               self.consumidor,
                                               self.data_criacao)

    def get_absolute_url(self):
        return '/minhas-listas/{}'.format(self.id)


class ProdutoLista(models.Model):
    class Meta:
        verbose_name = u'Produto em Lista'
        verbose_name_plural = u'Produtos em Lista'
    lista_compras = models.ForeignKey(ListaCompras)
    produto = models.ForeignKey(Produto)
    quantidade = models.IntegerField()


class Compra(models.Model):
    PAGAMENTOS_POSSIVEIS = (
                            ('cc', u'Cartao de Credito'),
                            ('cd', u'Cartao de Debito'),
                            ('di', u'Dinheiro'))
    consumidor = models.ForeignKey(Consumidor)
    supermercado = models.ForeignKey(Supermercado)
    produtos = models.ManyToManyField(Produto, through='ProdutoCompra')
    modo_pagamento = models.CharField(max_length=3,
                                      choices=PAGAMENTOS_POSSIVEIS)
    data_compra = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return "Compra de {} em {} na data {}".format(self.comprador,
                                                      self.supermercado,
                                                      self.data_compra)


class ProdutoCompra(models.Model):
    class Meta:
        verbose_name = u'Produto Comprado'
        verbose_name_plural = u'Produtos Comprados'
    compra = models.ForeignKey(Compra)
    produto = models.ForeignKey(Produto)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(decimal_places=2, max_digits=5)

    def __unicode__(self):
        return "{} na compra {}".format(self.produto,
                                        self.compra.id)

    def preco_total(self):
        return self.preco_unitario * self.quantidade


class ProdutoSupermercado(models.Model):
    produto = models.ForeignKey(Produto)
    supermercado = models.ForeignKey(Supermercado)
    preco = models.DecimalField(decimal_places=2, max_digits=5)
    quantidade = models.IntegerField()
    data_adicao = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{} em {} em {}".format(self.produto,
                                       self.supermercado,
                                       self.data_adicao)


class CarrinhoCompras(models.Model):
    supermercado = models.ForeignKey(Supermercado, null=True)
    usuario = models.OneToOneField(User)
    produtos = models.ManyToManyField(ProdutoSupermercado, through='ProdutoCarrinho')

    def gerar_botao_pagamento(self):
        context = Context({'carrinho': self})
        return get_template('cliente/_carrinho-form.html').render(context)
    
    def gerar_lista_compras(self):
        pass


class ProdutoCarrinho(models.Model):
    produto = models.ForeignKey(ProdutoSupermercado)
    carrinho = models.ForeignKey(CarrinhoCompras)
    quantidade = models.IntegerField()