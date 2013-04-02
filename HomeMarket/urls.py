from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'marketapp.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
        (r'^contas/', include('allauth.urls')),
    )