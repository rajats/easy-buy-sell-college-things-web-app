from django.db import models
from django.contrib.auth.models import User

from products.models import Product
from .signals import update_total_products, update_total_orders, new_user_profile, update_total_sold_products

class UserProfile(models.Model):
	user = models.ForeignKey(User)
	total_products = models.IntegerField(default=0)
	total_orders = models.IntegerField(default=0)
	total_sold_products = models.IntegerField(default=0)

	def __unicode__(self):
		return str(self.user)

class UserOrderedProducts(models.Model):
	profile = models.ForeignKey(UserProfile)
	order = models.ForeignKey(Product, null=True, blank=True)

class UserSoldProducts(models.Model):
	profile = models.ForeignKey(UserProfile)
	sold_product = models.ForeignKey(Product, null=True, blank=True)
		
def update_profile_products(sender, **kwargs):
	kwargs.pop('signal', None)
	profile = UserProfile.objects.get(user = sender)
	profile.total_products += 1
	profile.save()

update_total_products.connect(update_profile_products)

def update_profile_orders(sender, **kwargs):
	kwargs.pop('signal', None)
	product = kwargs.pop("ordered_product")
	profile = UserProfile.objects.get(user=sender)
	profile.total_orders += 1
	UserOrderedProducts.objects.create(profile=profile, order=product)
	profile.save()

update_total_orders.connect(update_profile_orders)

def update_sold_products(sender, **kwargs):
	kwargs.pop('signal', None)
	product = kwargs.pop("sold_product")
	profile = UserProfile.objects.get(user=sender)
	profile.total_sold_products += 1
	UserSoldProducts.objects.create(profile=profile, sold_product=product)
	profile.save()

update_total_sold_products.connect(update_sold_products)

def add_new_user_profile(sender, **kwargs):
	kwargs.pop('signal', None)
	UserProfile.objects.create(user=sender)

new_user_profile.connect(add_new_user_profile)
