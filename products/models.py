from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.files.storage import FileSystemStorage
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image


#protected_loc = settings.PROTECTED_UPLOADS

#def download_loc(instace, filename):
#	if instace.user.username:
#		return "%s/download/%s" %(instance.user.username, filename)
#	else:
#		return "%s/download/%s" %("default", filename)
# Create your models here.
class Product(models.Model):
	user = models.ForeignKey(User, null=True, blank=True)   #if we are adding products we can leave it null
														  #but if seller student is adding it can be null
	title = models.CharField(max_length=200)
	description = models.CharField(max_length=500)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False)
	slug = models.SlugField()
	order = models.IntegerField(default=0)
	active = models.BooleanField(default=True)
	ownercollege = models.CharField(max_length=50)
	ownerphone = models.CharField(max_length=10)

	def __unicode__(self):
		return str(self.title)

	class Meta:
		ordering=['-order']

	
	def get_price(self):
		if self.sale_price > 0:
			return "Actual price is :%s You get it for: %s" %(self.price, self.sale_price)
		else:
			return "You get it for: %s"%(self.price)
	def get_absolute_url(self):
		return reverse('single_product', args = [self.slug])                #single_product name of url

	def is_active(self):
		return self.active

class ProductImage(models.Model):
	product = models.ForeignKey(Product)   #multiple images can be linked to one product,for only one image use onetoonefield
	image = models.ImageField(upload_to="products/image/")
	title = models.CharField(max_length=200, null=True, blank=True)
	featured_image=models.BooleanField(default=False)

	def __unicode__(self):
		return str(self.title)

class Category(models.Model):
	product = models.ManyToManyField(Product)
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=500)
	slug = models.SlugField()

	def __unicode__(self):
		return str(self.title)

	class Meta:
		verbose_name = "category"
		verbose_name_plural = "categories"

class ProductComment(models.Model):
	product = models.ForeignKey(Product)
	commenter = models.CharField(max_length=50, default='')
	comment = models.TextField(max_length=1000, null=True, blank=True)
	pub_date = models.DateTimeField('date published')







