from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'marketapp.views.supermercado.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^contas/', include('allauth.urls')),
    url(r'^criar/$', 'marketapp.views.supermercado.adicionar_produto'),
    url(r'^criar_produto', 'marketapp.views.supermercado.criar_produto'),
    url(r'^adicionar-produto-existente/(?P<codigo>.*)',
        'marketapp.views.supermercado.adicionar_produto_existente'),
    url(r'^supermercado/(?P<nome>.*)$','marketapp.views.cliente.ver_produtos_supermercado')
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )