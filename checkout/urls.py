from django.conf.urls import patterns, include, url
from django.conf import settings 



urlpatterns = patterns('checkout.views',
	url(r'^(?P<slug>.*)/buy/','buy', name="buy"),
)

