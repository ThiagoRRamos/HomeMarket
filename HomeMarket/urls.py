from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'marketapp.views.geral.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^contas/', include('allauth.urls')),
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
    url(r'^home-cliente/$',
        'marketapp.views.cliente.home'),
    url(r'^supermercado/(?P<nome>.*)$',
        'marketapp.views.cliente.ver_produtos_supermercado'),
    url(r'^colocar-no-carrinho/(?P<produto_id>\d+)',
        'marketapp.views.cliente.adicionar_produto_carrinho'),
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
    url(r'^comparar-preco-supermercados/$',
        'marketapp.views.supermercado.comparar_produto_preco'),
    url(r'^definir-regiao/$',
        'marketapp.views.supermercado.definir_regiao_atendida'),
    url(r'^comprar/dinheiro/(?P<compra_id>\d+)$',
        'marketapp.views.cliente.pagamento_dinheiro'),
    url('^status-compras/$',
        'marketapp.views.supermercado.status_compras'),
    url('^atualizar-compra/(?P<compra_id>\d+)$',
        'marketapp.views.supermercado.atualizar_status')
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
