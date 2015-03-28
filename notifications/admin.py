from django.contrib import admin
from .models import Notification, NotifyUsers

admin.site.register(Notification)
admin.site.register(NotifyUsers)