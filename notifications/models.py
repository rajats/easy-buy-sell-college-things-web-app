from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from .signals import notify

# Create your models here.


class NotificationQuerySet(models.query.QuerySet):
	def get_user(self, receiver_user):
		return self.filter(receiver_user=receiver_user)

	def unread(self):
		return self.filter(read=False)

	def read(self):
		return self.filter(read=True)

	def mark_all_read(self, receiver_user):
		qs = self.unread().get_user(receiver_user)
		qs.update(read=True)

	def mark_all_unread(self, receiver_user):
		qs = self.read().get_user(receiver_user)
		qs.update(read=False)


class NotificationManager(models.Manager):
	def get_queryset(self):
		return NotificationQuerySet(self.model, using=self._db)

	def all_unread(self, user):
		return self.get_queryset().get_user(user).unread()

	def all_read(self, user):
		return self.get_queryset().get_user(user).read()

	def all_for_user(self, user):
		return self.get_queryset().get_user(user)






class Notification(models.Model):
	#sender = models.ForeignKey()

	sender_content_type = models.ForeignKey(ContentType, related_name='nofity_sender')
	sender_object_id = models.PositiveIntegerField()
	sender_object = generic.GenericForeignKey("sender_content_type", "sender_object_id")
	
	msg = models.CharField(max_length=500)

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

	objects = NotificationManager()

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
			if self.action_object and not target_url:
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
			return "<a href='%(target_url)s'>%(sender)s %(msg)s %(target)s with %(action)s </a>" %context
		else:
			return "<a href='%(target_url)s'>%(sender)s %(msg)s </a>" %context


#this is the receiver function for notify signal
def new_notification(sender, **kwargs):                
	kwargs.pop('signal', None)
	receiver_user = kwargs.pop("receiver_user")
	msg = kwargs.pop("msg")
	target = kwargs.pop("target", None)
	action = kwargs.pop("action", None)
	new_note = Notification(
		receiver_user=receiver_user,
		msg = msg, 
		sender_content_type = ContentType.objects.get_for_model(sender),
		sender_object_id = sender.id,
		)
	#for option in ("action"):
	#	obj = kwargs.pop(option, None)
	#	if obj is not None:
	#		setattr(new_note, "%s_content_type" %option, ContentType.objects.get_for_model(obj))
	#		setattr(new_note, "%s_object_id" %option, obj.id)
	
	if action is not None:
		new_note.action_content_type = ContentType.objects.get_for_model(action)
		new_note.action_object_id = action.id

	if target is not None:
		new_note.target_content_type = ContentType.objects.get_for_model(target)
		new_note.target_object_id = target.id


	new_note.save()
	print new_note


notify.connect(new_notification)