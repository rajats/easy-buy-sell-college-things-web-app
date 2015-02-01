from django.db import models
from products.models import Product
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.db.models import signals
from products.models import Product
# Create your models here.

class Cart(models.Model):
	user = models.ForeignKey(User, null = True, blank = True)
	total = models.DecimalField(max_digits=10, default = 0, decimal_places=2)
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return str(self.id)
	
class CartItem(models.Model):
	cart = models.ForeignKey(Cart)
	product = models.ForeignKey(Product)
	#quantity = models.IntegerField(default = 0)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return "%s" %(self.product.title)

@receiver([signals.post_save, signals.post_delete], sender=CartItem)
def calculate_total(sender, instance, **kwargs):
	cart = instance.cart
	totals = []
	for item in cart.cartitem_set.all():
		if item.product.sale_price > 0:
			totals.append(item.product.sale_price)  
		else:
			totals.append(item.product.price)
	cart.total = sum(totals)
	cart.save()

#signas.post_save.connect(calculate_total, sender = CartItem)
#signas.post_delete.connect(calculate_total, sender = CartItem)
