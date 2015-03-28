from django.conf.urls import patterns, include, url
from django.conf import settings 

urlpatterns = patterns('cart.views',
	url(r'^$','cart', name="cart"), 
    url(r'^add/(?P<id>.*)','add_to_cart', name="add_to_cart"),
    url(r'^delete/(?P<id>.*)','delete_from_cart', name="delete_from_cart"),
)
