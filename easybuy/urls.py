from django.conf.urls import patterns, include, url
from django.conf import settings 
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework import routers

from products.serializers import ProductViewSet
from products.serializers import ProductCommentsViewSet

router = routers.DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"comments", ProductCommentsViewSet)

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','easybuy.views.home', name="home"),           #this home page url
    url(r'^recent/','easybuy.views.morerecents', name="morerecents"),
    url(r'^lib/','profiles.views.library', name="library"),
    (r'^products/', include('products.urls')),
    (r'^cart/', include('cart.urls')),
    (r'^notifications/', include('notifications.urls')),
    (r'^userauth/', include('userauth.urls')),
    (r'^checkout/', include('checkout.urls')),
    (r'^accounts/', include('allauth.urls')),
    (r'^profiles/', include('profiles.urls')),
    (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root: settings.STATIC_ROOT'}),
    (r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root: settings.MEDIA_ROOT'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/auth/token/$', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),     #this enables login in rest framework
    url(r'^api/', include(router.urls)),
)
