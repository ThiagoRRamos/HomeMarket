from django.contrib.auth.models import User
from django.db import models
from django.template.context import Context
from django.template.loader import get_template
from taggit.managers import TaggableManager


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
    imagem = models.ImageField(upload_to="produtos",
                               default="examples/produto.jpg")
    nome = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    descricao = models.TextField()
    codigo_de_barras = models.CharField(max_length=15, unique=True)
    categoria = models.ForeignKey(Categoria)
    quantidade = models.IntegerField()
    quantidade_unidade = models.CharField(max_length=5,
                                          choices=UNIDADES)
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self):
        return '/ver-produto/{}'.format(self.id)

    def limites_preco(self):
        if not ProdutoSupermercado.objects.filter(produto=self).exists():
            return (0, 0)
        minimo = min(ProdutoSupermercado.objects.filter(produto=self),
                     key=lambda x: x.preco).preco
        maximo = max(ProdutoSupermercado.objects.filter(produto=self),
                     key=lambda x: x.preco).preco
        return (minimo, maximo)


class Consumidor(models.Model):

    class Meta:
        verbose_name_plural = u'Consumidores'

    usuario = models.OneToOneField(User)
    cpf = models.CharField(max_length=20)
    cep = models.CharField(max_length=10)
    telefone = models.CharField(max_length=20)

    def __unicode__(self):
        return self.usuario.username


class Supermercado(models.Model):
    usuario = models.OneToOneField(User)
    nome_exibicao = models.CharField(max_length=50)
    nome_url = models.SlugField()
    chave_bcash = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nome_exibicao

    def get_absolute_url(self):
        return '/supermercado/{}'.format(self.nome_url)


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
    def get_nome(self):    
        return self.produto.nome
    def get_preco(self):
        return self.preco
    
    def get_imagem(self):
        return self.produto.imagem
    
    def get_absolute_url(self):
        return self.produto.get_absolute_url()

class PromocaoCombinacao(models.Model):
    nome = models.TextField()
    produtos = models.ManyToManyField(ProdutoSupermercado)
    desconto = models.IntegerField()
    supermercado = models.ForeignKey(Supermercado)
    quantidade = models.IntegerField()
    imagem = models.ImageField(upload_to="produtos",
                               default="examples/produto.jpg")
    data_adicao = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{} em {} em {}".format(self.nome, self.supermercado,
                                       self.data_adicao)
    def get_nome(self):
        return self.nome
    def get_preco(self):
        preco = 0
        for p in self.produtos.all():
            preco += p.preco
        preco *= 1 - self.desconto / 100
        return preco
   
    def get_imagem(self):
        return self.imagem
    
    def get_absolute_url(self):
        return '/ver-promocao/{}'.format(self.id)
    
class RegiaoAtendida(models.Model):
    supermercado = models.ForeignKey(Supermercado)
    cep_inicio = models.CharField(max_length=10)
    cep_final = models.CharField(max_length=10)
    preco = models.DecimalField(decimal_places=2, max_digits=4)
    tempo = models.IntegerField()


class ListaCompras(models.Model):
    class Meta:
        verbose_name = u'Lista de Compras'
        verbose_name_plural = u'Listas de Compras'
    nome = models.CharField(max_length=50)
    consumidor = models.ForeignKey(Consumidor)
    produtos = models.ManyToManyField(ProdutoSupermercado,
                                      through='ProdutoLista')
    data_criacao = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return "Lista '{}' de {}".format(self.nome,
                                         self.data_criacao)

    def get_absolute_url(self):
        return '/minhas-listas/{}'.format(self.id)


class ProdutoLista(models.Model):
    class Meta:
        verbose_name = u'Produto em Lista'
        verbose_name_plural = u'Produtos em Lista'
    lista_compras = models.ForeignKey(ListaCompras)
    produto = models.ForeignKey(ProdutoSupermercado)
    quantidade = models.IntegerField()


class Compra(models.Model):
    PAGAMENTOS_POSSIVEIS = (('cc', u'Cartao de Credito'),
                            ('cd', u'Cartao de Debito'),
                            ('di', u'Dinheiro'),
                            ('nn', u'Nao definido'))
    STATUS_PAGAMENTOS = (('pn', 'Pagamento nao iniciado'),
                         ('pi', 'Pagamento Iniciado'),
                         ('pa', 'Pagamento Aprovado'),
                         ('pc', 'Pagamento Cancelado'),
                         ('pd', 'Pagamento em Dinheiro'),
                         ('ei', 'Entrega Iniciada'),
                         ('et', 'Entrega em Transporte'),
                         ('ee', 'Entrega Entregue'),)

    consumidor = models.ForeignKey(Consumidor)
    supermercado = models.ForeignKey(Supermercado)
    produtos = models.ManyToManyField(ProdutoSupermercado,
                                      through='ProdutoCompra')
    modo_pagamento = models.CharField(max_length=3,
                                      choices=PAGAMENTOS_POSSIVEIS)
    status_pagamento = models.CharField(max_length=3,
                                        choices=STATUS_PAGAMENTOS)
    data_compra = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return "Compra de {} em {} na data {}".format(self.consumidor,
                                                      self.supermercado,
                                                      self.data_compra)

    def gerar_botao_pagamento(self):
        context = Context({'carrinho': self})
        return get_template('cliente/_carrinho-form.html').render(context)

class CompraAgendada(models.Model):
    PAGAMENTOS_POSSIVEIS = (('cc', u'Cartao de Credito'),
                            ('cd', u'Cartao de Debito'),
                            ('di', u'Dinheiro'),
                            ('nn', u'Nao definido'))
    STATUS_PAGAMENTOS = (('pn', 'Pagamento nao iniciado'),
                         ('pi', 'Pagamento Iniciado'),
                         ('pa', 'Pagamento Aprovado'),
                         ('pc', 'Pagamento Cancelado'),
                         ('pd', 'Pagamento em Dinheiro'),
                         ('ei', 'Entrega Iniciada'),
                         ('et', 'Entrega em Transporte'),
                         ('ee', 'Entrega Entregue'),)

    consumidor = models.ForeignKey(Consumidor)
    supermercado = models.ForeignKey(Supermercado)
    produtos = models.ManyToManyField(ProdutoSupermercado,
                                      through='ProdutoCompraAgendada')
    modo_pagamento = models.CharField(max_length=3,
                                      choices=PAGAMENTOS_POSSIVEIS)
    status_pagamento = models.CharField(max_length=3,
                                        choices=STATUS_PAGAMENTOS)
    data_compra = models.DateField(auto_now_add=True)
    data_entrega = models.DateField();

    def __unicode__(self):
        return "Compra de {} em {} na data {}".format(self.consumidor,
                                                      self.supermercado,
                                                      self.data_compra)



class ProdutoCompra(models.Model):
    class Meta:
        verbose_name = u'Produto Comprado'
        verbose_name_plural = u'Produtos Comprados'
    compra = models.ForeignKey(Compra)
    produto = models.ForeignKey(ProdutoSupermercado)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(decimal_places=2, max_digits=5)

    def __unicode__(self):
        return "{} na compra {}".format(self.produto,
                                        self.compra.id)

    def preco_total(self):
        return self.preco_unitario * self.quantidade

class ProdutoCompraAgendada(models.Model):
    class Meta:
        verbose_name = u'Produto Comprado'
        verbose_name_plural = u'Produtos Comprados'
    compra = models.ForeignKey(CompraAgendada)
    produto = models.ForeignKey(ProdutoSupermercado)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(decimal_places=2, max_digits=5)

    def __unicode__(self):
        return "{} na compra {}".format(self.produto,
                                        self.compra.id)

    def preco_total(self):
        return self.preco_unitario * self.quantidade


class CarrinhoCompras(models.Model):
    supermercado = models.ForeignKey(Supermercado, null=True)
    usuario = models.OneToOneField(User)
    produtos = models.ManyToManyField(ProdutoSupermercado,
                                      through='ProdutoCarrinho')

    def gerar_lista_compras(self, nome=None):
        if not nome:
            nome = "Lista de " + str(self)
        lista = ListaCompras.objects.create(nome=nome,
                                            consumidor=self.usuario.consumidor)
        for p in self.produtocarrinho_set.all():
            ProdutoLista.objects.create(lista_compras=lista,
                                        produto=p.produto,
                                        quantidade=p.quantidade)
        return lista

    def total(self):
        return sum((p.quantidade * p.produto.preco for p in self.produtocarrinho_set.all()))


class ProdutoCarrinho(models.Model):
    produto = models.ForeignKey(ProdutoSupermercado)
    carrinho = models.ForeignKey(CarrinhoCompras)
    quantidade = models.IntegerField()
