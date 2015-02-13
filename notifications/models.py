from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from .signals import notify

# Create your models here.

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

	#read
	#unread
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __unicode__(self):
		return str(self.msg)


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