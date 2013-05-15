'''
Created on Apr 3, 2013

@author: thiagorramos
'''
from marketapp.models import ProdutoSupermercado, Produto, Consumidor
from django.forms.models import ModelForm
from django import forms


class RegistroUsuario(forms.Form):
    cpf = forms.CharField()
    cep = forms.CharField()

    def save(self, user):
        Consumidor.objects.create(usuario=user,
                                  cpf=self.cleaned_data['cpf'],
                                  cep=self.cleaned_data['cep'])


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
