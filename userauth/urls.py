from django.conf.urls import patterns, include, url
from django.conf import settings 



urlpatterns = patterns('userauth.views',
    url(r'^login/','signin', name="login"),
    url(r'^logout/','signout', name="logout"),
    url(r'^register/','register', name="register"),
)
