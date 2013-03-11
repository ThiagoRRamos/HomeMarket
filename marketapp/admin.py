from django.contrib import admin
from marketapp.models import Categoria, Produto, Consumidor, Supermercado,\
    ListaCompras, AdicaoProduto, Compra, ProdutoSupermercado

admin.site.register(Categoria)
admin.site.register(Produto)
admin.site.register(Consumidor)
admin.site.register(Supermercado)
admin.site.register(ListaCompras)
admin.site.register(AdicaoProduto)
admin.site.register(Compra)
admin.site.register(ProdutoSupermercado)
