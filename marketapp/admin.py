from django.contrib import admin
from marketapp.models import Categoria, Produto, Consumidor, Supermercado,\
    ListaCompras, Compra, ProdutoSupermercado, CarrinhoCompras, ProdutoCarrinho,\
    RegiaoAtendida, CompraAgendada, AvaliacaoSupermercado, PromocaoCombinacao,\
    ProdutoCompra

admin.site.register(Categoria)
admin.site.register(Produto)
admin.site.register(Consumidor)
admin.site.register(Supermercado)
admin.site.register(ListaCompras)
admin.site.register(Compra)
admin.site.register(ProdutoSupermercado)
admin.site.register(CarrinhoCompras)
admin.site.register(ProdutoCarrinho)
admin.site.register(RegiaoAtendida)
admin.site.register(CompraAgendada)
admin.site.register(AvaliacaoSupermercado)
admin.site.register(PromocaoCombinacao)
admin.site.register(ProdutoCompra)

