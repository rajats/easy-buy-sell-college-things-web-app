from django.db import models
from products.models import Product
from django.contrib.auth.models import User
# Create your models here.

class Checkout:
	user = models.ForeignKey(User, null = True, blank = True)
	product = models.ForeignKey(Product)
	sold = models.BooleanField(default=False)

	def __unicode__(self):
		return str(self.id)
