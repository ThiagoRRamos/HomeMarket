from django.db import models
from django.contrib.auth.models import User


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
                ('kg', 'kg'))
    nome = models.CharField(max_length=50)
    descricao = models.TextField()
    codigo_de_barras = models.CharField(max_length=15)
    categoria = models.ForeignKey(Categoria)
    quantidade = models.IntegerField()
    quantidade_unidade = models.CharField(max_length=5,
                                          choices=UNIDADES)

    def __unicode__(self):
        return self.nome


class Consumidor(models.Model):
    usuario = models.OneToOneField(User)

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


class ListaCompras(models.Model):
    nome = models.CharField(max_length=50)
    consumidor = models.ForeignKey(Consumidor)
    produtos = models.ManyToManyField(Produto, through='AdicaoProduto')
    data_criacao = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return "Lista '{}' de {} de {}".format(self.nome,
                                               self.consumidor,
                                               self.data_criacao)

    def get_absolute_url(self):
        return '/minhas-listas/{}'.format(self.id)


class AdicaoProduto(models.Model):
    lista_compras = models.ForeignKey(ListaCompras)
    produto = models.ForeignKey(Produto)
    quantidade = models.IntegerField()


class Compra(models.Model):
    PAGAMENTOS_POSSIVEIS = (
                            ('cc',u'Cartao de Credito'),
                            ('cd',u'Cartao de Debito'),
                            ('di',u'Dinheiro'))
    comprador = models.ForeignKey(Consumidor)
    supermercado = models.ForeignKey(Supermercado)
    produtos = models.ManyToManyField(Produto, through='CompraProduto')
    modo_pagamento = models.CharField(max_length=5,
                                      choices=PAGAMENTOS_POSSIVEIS)
    data_compra = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return "Compra de {} em {} na data {}".format(self.comprador,
                                                      self.supermercado,
                                                      self.data_compra)


class CompraProduto(models.Model):
    compra = models.ForeignKey(Compra)
    produto = models.ForeignKey(Produto)
    quantidade = models.IntegerField()


class ProdutoSupermercado(models.Model):
    produto = models.ForeignKey(Produto)
    supermercado = models.ForeignKey(Supermercado)
    quantidade = models.IntegerField()
    limite_venda = models.DateField(blank=True)
