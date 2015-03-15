from django.conf.urls import patterns, include, url
from django.conf import settings 



urlpatterns = patterns('checkout.views',
	url(r'^(?P<slug>.*)/buy/','buy', name="buy"),
	url(r'^(?P<slug>.*)/confirmorder/','confirmorder', name="confirmorder"),
	url(r'^(?P<slug>.*)/rejectorder/','rejectorder', name="rejectorder"),
)

