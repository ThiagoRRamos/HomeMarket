'''
Created on May 15, 2013

@author: thiagorramos
'''
from marketapp.models import Produto
from haystack import indexes

class ProdutoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    nome = indexes.CharField(model_attr='categoria')
    categoria = indexes.CharField(model_attr='categoria')
    marca = indexes.CharField(model_attr='marca')
    
    def get_model(self):
        return Produto
    
    def index_queryset(self, using=None):
        return self.get_model().objects.all()