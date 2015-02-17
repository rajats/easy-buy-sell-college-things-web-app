from django.forms import ModelForm
from .models import Product, ProductImage, ProductComment

class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = ('title','description','yearofpurchase','price','sale_price','ownercollege','ownerphone')


class ProductImageForm(ModelForm):
	class Meta:
		model = ProductImage
		fields = ('image', 'featured_image', 'title')

class ProductCommentForm(ModelForm):
	class Meta:
		model = ProductComment
		fields = ( 'comment',)

class UnRegUserProductCommentForm(ModelForm):
	class Meta:
		model = ProductComment
		fields = ( 'commenter','comment',)

