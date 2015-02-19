from django.contrib import admin
from .models import Notification, NotifyUsers

# Register your models here.
admin.site.register(Notification)
admin.site.register(NotifyUsers)