from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from products.models import Product

from .signals import notify

# Create your models here.

class Notification(models.Model):
	sender_content_type = models.ForeignKey(ContentType, related_name='nofity_sender')
	sender_object_id = models.PositiveIntegerField()
	sender_object = generic.GenericForeignKey("sender_content_type", "sender_object_id")
	
	msg = models.CharField(max_length=500)
	signal_sender = models.ForeignKey(ContentType, related_name='signal_sender',null=True, blank=True)

	action_content_type = models.ForeignKey(ContentType, related_name='notify_action', 
		null=True, blank=True)
	action_object_id = models.PositiveIntegerField(null=True, blank=True)
	action_object = generic.GenericForeignKey("action_content_type", "action_object_id")

	target_content_type = models.ForeignKey(ContentType, related_name='notify_target', 
		null=True, blank=True)
	target_object_id = models.PositiveIntegerField(null=True, blank=True)
	target_object = generic.GenericForeignKey("target_content_type", "target_object_id")


	receiver_user = models.ForeignKey(User, null=True, blank=True)

	read = models.BooleanField(default=False)

	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __unicode__(self):
		
		try:
			target_url = self.target_object.get_absolute_url()
		except:
			target_url = None

		context = {
			"sender": self.sender_object,
			"msg": self.msg,
			"action": self.action_object,
			"target": self.target_object,
			"target_url": target_url,
		}
		if self.target_object:
			if self.action_object and target_url:
				return "%(sender)s %(msg)s <a href='%(target_url)s'>%(target)s</a> with %(action)s" %context
			elif not self.action_object and target_url:
				return "%(sender)s %(msg)s <a href='%(target_url)s'>%(target)s</a>" %context
			elif self.action_object and not target_url:
				return "%(sender)s %(msg)s %(target)s with %(action)s" %context
			return "%(sender)s %(msg)s %(target)s" %context
		return "%(sender)s %(msg)s" %context


	def get_link(self):
		
		try:
			target_url = self.target_object.get_absolute_url()
		except:
			target_url = reverse("notifications_all")

		context = {
			"sender": self.sender_object,
			"msg": self.msg,
			"action": self.action_object,
			"target": self.target_object,
			"target_url": target_url,
		}
		if self.target_object:
			if self.action_object:
				return "<a href='%(target_url)s'>%(sender)s %(msg)s %(target)s with %(action)s </a>" %context
			else:
				return "<a href='%(target_url)s'>%(sender)s %(msg)s %(target)s </a>" %context
		else:
			return "<a href='%(target_url)s'>%(sender)s %(msg)s </a>" %context


class NotifyUsers(models.Model):
	sender = models.ForeignKey(User, null=True, blank=True,  related_name='sender')
	user = models.ForeignKey(User, null=True, blank=True,  related_name = 'receiver')
	notifications = models.ForeignKey(Notification)
	product = models.ForeignKey(Product, null=True, blank=True)
	read = models.BooleanField(default=False)
	buy_request = models.BooleanField(default=False)


#this is the receiver function for notify signal
def new_notification(sender, **kwargs):                
	kwargs.pop('signal', None)
	receiver_user = kwargs.pop("receiver_user")
	msg = kwargs.pop("msg")
	target = kwargs.pop("target", None)
	action = kwargs.pop("action", None)
	signal_sender = kwargs.pop("signal_sender")
	new_note = Notification(
		receiver_user=receiver_user,
		msg = msg, 
		sender_content_type = ContentType.objects.get_for_model(sender),
		sender_object_id = sender.id,
		signal_sender = ContentType.objects.get_for_model(signal_sender),
		)	
	if action is not None:
		new_note.action_content_type = ContentType.objects.get_for_model(action)
		new_note.action_object_id = action.id

	if target is not None:
		new_note.target_content_type = ContentType.objects.get_for_model(target)
		new_note.target_object_id = target.id


	new_note.save()
	product = Product.objects.get(id = target.id)
	sender = User.objects.get(id = sender.id)
	NotifyUsers.objects.create(sender = sender, user = receiver_user, notifications = new_note, product = product)


notify.connect(new_notification)