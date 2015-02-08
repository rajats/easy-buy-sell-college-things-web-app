import random
from django.contrib import admin
admin.autodiscover()

# Register your models here.
from .models import Product, Category, ProductImage, ProductComment


class ProductImageInline(admin.TabularInline):    #so that u can add evrything related to product at one place
	model = ProductImage

class ProductCommentInline(admin.TabularInline):    #so that u can add evrything related to product at one place
	model = ProductComment


class ProductAdmin(admin.ModelAdmin):
	list_display = ('__unicode__','description','current_price','order', 'categories', 'live_link')
	inlines = [ProductImageInline, ProductCommentInline]      #so that u can add evrything related to product at one place
	search_fields = ['title', 'description','price', 'category__title']    #you can search product by their these fileds
	list_filter = ['price', 'sale_price']        #these will appear as box in right

	prepopulated_fields = {"slug":('title',)}          #it will prepopulate slug with text given in title
	readonly_fields=['categories', 'live_link']
	class Meta:
		model = Product

	def current_price(self, object):
		if object.sale_price > 0:
			return object.sale_price
		else:
			return object.price

	def categories(self, object):
		categs = []
		for element in object.category_set.all():     #it will return list of all foreign keys it is associated to
			link = "<a href='/admin/products/category/" +str(element.id) +  "/'>" + element.title + "</a>"
			categs.append(link)
		return ", ".join(categs)
	categories.allow_tags = True     #to make links working

	def live_link(self, object):
		link = "<a href='/products/" +str(object.slug) +  "/'>" + object.title + "</a>"
		return link
	live_link.allow_tags = True     #to make links working

admin.site.register(Product, ProductAdmin)
		

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug":('title',)}
	class Meta:
		model = Category
admin.site.register(Category, CategoryAdmin)		