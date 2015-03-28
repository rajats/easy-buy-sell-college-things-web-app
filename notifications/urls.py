from django.conf.urls import patterns, include, url
from django.conf import settings 

urlpatterns = patterns('notifications.views',
    url(r'^$','all', name="notifications_all"),
    url(r'^ajax/$', 'get_notifications_using_ajax', name='get_notifications_using_ajax'),
    url(r'^markallread/$', 'mark_all_as_read', name='mark_all_as_read'),
)
