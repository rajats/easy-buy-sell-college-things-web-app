from django.db import models
from django.contrib.auth.models import User

from products.models import Product
from .signals import update_total_products, update_total_orders

class UserProfile(models.Model):
	user = models.ForeignKey(User)
	total_products = models.IntegerField(default=0)
	total_orders = models.IntegerField(default=0)

	def __unicode__(self):
		return str(self.user)

class UserOrderedProducts(models.Model):
	profile = models.ForeignKey(UserProfile)
	order = models.ForeignKey(Product, null=True, blank=True)
		
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
