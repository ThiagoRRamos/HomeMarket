from django.conf.urls import patterns, include, url
from django.contrib import admin
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView
from marketapp.services.analise_produto import is_disponivel
from marketapp.utils.autorizacao import eh_cliente
import settings


admin.autodiscover()

sqs = SearchQuerySet().facet('marca').facet('categoria')


class FacetedSearchViewComDisponibilidade(FacetedSearchView):

    def extra_context(self):
        extra = super(FacetedSearchViewComDisponibilidade, self).extra_context()
        for r in self.results:
            if eh_cliente(self.request.user):
                r.object.disp = is_disponivel(r.object, self.request.user.consumidor)
        return extra

urlpatterns = patterns('',
    #Views gerais
    url(r'^$', 'marketapp.views.geral.home', name='home'),
    url('^ver-produto/(?P<produto_id>\d+)$',
        'marketapp.views.geral.ver_produto'),
    url('^ver-promocao/(?P<promocaoCombinacao_id>\d+)$',
        'marketapp.views.geral.ver_promocao'),                   
    (r'^contas/', include('allauth.urls')),
    url(r'^busca/$',
        FacetedSearchViewComDisponibilidade(form_class=FacetedSearchForm,
                                            searchqueryset=sqs),
        name='haystack_search'),
    #Views de admin
    url(r'^admin/', include(admin.site.urls)),
    #Views de supermercados
    url(r'^criar/$',
        'marketapp.views.supermercado.adicionar_produto'),
    url(r'^criar_produto',
        'marketapp.views.supermercado.criar_produto'),
    url(r'^adicionar-produto-existente/(?P<codigo>.*)',
        'marketapp.views.supermercado.adicionar_produto_existente'),
    url(r'^modificar-preco-existente/(?P<codigo>.*)',
        'marketapp.views.supermercado.modificar_preco_existente'),
    url(r'^modificar-preco/$',
        'marketapp.views.supermercado.modificar_preco'),
    url(r'^home-supermercado/$',
        'marketapp.views.supermercado.home'),
    url(r'^comparar-preco-supermercados/$',
        'marketapp.views.supermercado.comparar_produto_preco'),
    url(r'^definir-regiao/$',
        'marketapp.views.supermercado.definir_regiao_atendida'),
    url('^status-compras/$',
        'marketapp.views.supermercado.status_compras'),
    url('^atualizar-compra/(?P<compra_id>\d+)$',
        'marketapp.views.supermercado.atualizar_status'),
    #Views de clientes
    url(r'^home-cliente/$',
        'marketapp.views.cliente.home'),
    url(r'^supermercado/(?P<nome>.*)$',
        'marketapp.views.cliente.ver_produtos_supermercado'),
    url(r'^colocar-no-carrinho/(?P<produto_id>\d+)',
        'marketapp.views.cliente.adicionar_produto_carrinho'),
    url(r'^json/colocar-no-carrinho/(?P<produto_id>\d+)',
        'marketapp.views.cliente.json_adicionar_produto_carrinho'),
    url(r'^meu-carrinho/$',
        'marketapp.views.cliente.ver_carrinho'),
    url(r'^comprar/$',
        'marketapp.views.cliente.pagina_compra'),
    url(r'^meu-carrinho/apagar$',
        'marketapp.views.cliente.apagar_carrinho'),
    url(r'^meu-carrinho/remover-produto/(?P<produtocarrinho_id>\d+)$',
        'marketapp.views.cliente.remover_produto_carrinho'),
    url(r'^comparar-supermercados/$',
        'marketapp.views.cliente.comparar_supermercados'),
    url(r'^comprar/dinheiro/(?P<compra_id>\d+)$',
        'marketapp.views.cliente.pagamento_dinheiro'),
    url('^meu-carrinho/gerar-lista$',
        'marketapp.views.cliente.gerar_lista'),
    url('^completar-compra/(?P<compra_id>\d+)$',
        'marketapp.views.cliente.completar_compra'),
    url(r'^historico/$',
        'marketapp.views.cliente.ver_historico_compras'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
