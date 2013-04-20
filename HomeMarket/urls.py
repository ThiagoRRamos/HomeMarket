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
    url(r'^supermercado/(?P<nome>.*)$',
        'marketapp.views.cliente.ver_produtos_supermercado'),
    url(r'^home-supermercado',
        'marketapp.views.supermercado.home'),
    url(r'^colocar-no-carrinho/(?P<produto_id>\d+)',
        'marketapp.views.cliente.adicionar_produto_carrinho'),
    url(r'^meu-carrinho/$',
        'marketapp.views.cliente.ver_carrinho'),
    url(r'^comparar-supermercados/$',
        'marketapp.views.cliente.comparar_supermercados'),
    url(r'^comparar-preco-supermercados/$',
        'marketapp.views.supermercado.comparar_produto_preco')
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
