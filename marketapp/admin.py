from django.contrib import admin
from marketapp.models import Categoria, Produto, Consumidor, Supermercado, \
    ListaCompras, Compra, ProdutoSupermercado, CarrinhoCompras, ProdutoCarrinho, \
    RegiaoAtendida, CompraAgendada, AvaliacaoSupermercado, PromocaoCombinacao, \
    ProdutoCompra, CompraRecorrente, PromocaoSimples, PromocaoAtacado

admin.site.register(Categoria)
admin.site.register(Produto)


class ConsumidorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cep', 'cpf', 'telefone')

admin.site.register(Consumidor, ConsumidorAdmin)


admin.site.register(Supermercado)
admin.site.register(ListaCompras)
admin.site.register(Compra)
admin.site.register(ProdutoSupermercado)
admin.site.register(CarrinhoCompras)
admin.site.register(ProdutoCarrinho)


class RegiaoAtendidaAdmin(admin.ModelAdmin):
    list_display = ('supermercado', 'cep_inicio', 'cep_final', 'preco', 'tempo')
    ordering = ('supermercado',)

admin.site.register(RegiaoAtendida, RegiaoAtendidaAdmin)
admin.site.register(CompraAgendada)
admin.site.register(CompraRecorrente)


class AvaliacaoSupermercadoAdmin(admin.ModelAdmin):
    list_display = ('consumidor', 'supermercado', 'nota')

admin.site.register(AvaliacaoSupermercado, AvaliacaoSupermercadoAdmin)
admin.site.register(ProdutoCompra)

admin.site.register(PromocaoCombinacao)
admin.site.register(PromocaoSimples)
admin.site.register(PromocaoAtacado)
