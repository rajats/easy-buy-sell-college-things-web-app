from django.conf.urls import patterns, include, url
from django.conf import settings 

urlpatterns = patterns('profiles.views',
	url(r'^/userprofile/$','library', name="library"),
)