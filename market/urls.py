from django.conf.urls import patterns, include, url
from django.conf import settings 
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'esell.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #without regular expression you cant use css,javascript..
    url(r'^$','market.views.home', name="home"),           #this home page url
    url(r'^recent/','market.views.morerecents', name="morerecents"),
    url(r'^lib/','profiles.views.library', name="library"),
    (r'^products/', include('products.urls')),
    (r'^cart/', include('cart.urls')),
    (r'^userauth/', include('userauth.urls')),
    #url(r'^products/(?P<slug>.*)/$', 'products.views.single', name="single"),
    (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root: settings.STATIC_ROOT'}),
    (r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root: settings.MEDIA_ROOT'}),
    url(r'^admin/', include(admin.site.urls)),
)
