from django.db import models
from django.contrib.auth.models import User

from .signals import notify

# Create your models here.

class Notification(models.Model):
	#sender = models.ForeignKey()
	receiver_user = models.ForeignKey(User, null=True, blank=True)
	action = models.CharField(max_length = 500)
	#read
	#unread
	timestamp = models.DateTimeField()

	def __unicode__(self):
		return str(self.action)


#this is the receiver function for notify signal
def new_notification(sender, receiver_user, action, *args, **kwargs):                
	create_notification = Notification.objects.create(receiver_user = receiver_user, action = action)
	print receiver_user
	print action
	print args
	print kwargs


notify.connect(new_notification)