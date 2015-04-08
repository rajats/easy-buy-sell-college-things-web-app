from django.forms import ModelForm

from .models import Product, ProductImage, ProductComments

class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = ('title','description','yearofpurchase','price','sale_price','ownercollege','ownerphone')

class ProductImageForm(ModelForm):
	class Meta:
		model = ProductImage
		fields = ('image', 'featured_image', 'title')

class ProductCommentsForm(ModelForm):
	class Meta:
		model = ProductComments
		fields = ( 'comment',)

class UnRegUserProductCommentsForm(ModelForm):
	class Meta:
		model = ProductComments
		fields = ( 'commenter','comment',)

