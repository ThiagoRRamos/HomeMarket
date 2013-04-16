'''
Created on Apr 3, 2013

@author: thiagorramos
'''
from marketapp.models import ProdutoSupermercado, Produto
from django.forms.models import ModelForm


class ProdutoForm(ModelForm):
    class Meta:
        model = Produto


class ProdutoSupermercadoForm(ModelForm):
    class Meta:
        model = ProdutoSupermercado
        exclude = ('produto', 'supermercado')


class ProdutoSupermercadoFormPreco(ModelForm):
    class Meta:
        model = ProdutoSupermercado
        exclude = ('produto', 'supermercado', 'quantidade', 'limite_venda')

