from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from products.models import Product
from .signals import page_view

class PageViewQuerySet(models.query.QuerySet):
	def products(self):
		content_type = ContentType.objects.get_for_model(Product)
		return self.filter(primary_content_type=content_type)

class PageViewManager(models.Manager):
	def get_queryset(self):
		return PageViewQuerySet(self.model, using=self._db)

	def get_products(self):
		return self.get_queryset().products()

class PageView(models.Model):
	path = models.CharField(max_length=350)
	user = models.ForeignKey(User, null=True, blank=True)
	primary_content_type = models.ForeignKey(ContentType, related_name='primary_obj',null=True, blank=True)
	primary_object_id = models.PositiveIntegerField(null=True, blank=True)
	primary_object = generic.GenericForeignKey("primary_content_type", "primary_object_id")
	timestamp = models.DateTimeField(default=timezone.now())
	objects = PageViewManager()

	def __unicode__(self):
		return self.path

	class Meta:
		ordering = ['-timestamp']

def page_view_received(sender, **kwargs):
	kwargs.pop('signal', None)
	page_path = kwargs.pop('page_path')
	primary_obj = kwargs.pop('primary_obj', None)
	user = sender
	if not user.is_authenticated():
		new_page_view = PageView.objects.create(path=page_path, timestamp=timezone.now())
	else:
		new_page_view = PageView.objects.create(path=page_path, user=user, timestamp=timezone.now())
	if primary_obj:
		new_page_view.primary_object_id = primary_obj.id
		new_page_view.primary_content_type = ContentType.objects.get_for_model(primary_obj)
		new_page_view.save()

page_view.connect(page_view_received)
