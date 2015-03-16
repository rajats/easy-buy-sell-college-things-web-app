
from django.shortcuts import render_to_response, RequestContext, Http404,HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from products.models import Product
from analysis.signals import page_view
from analysis.models import PageView

# Create your views here.

def home(request):
	if request.user.is_authenticated():
		all_recent_product_obj = request.user.pageview_set.get_products()[:3]
		unique_recent_products_obj = []
		for obj in all_recent_product_obj:
			if not obj.primary_object in unique_recent_products_obj:
				unique_recent_products_obj.append(obj.primary_object)
	else:
		all_recent_product_obj = PageView.objects.get_products()[:3]
		unique_recent_products_obj = []
		for obj in all_recent_product_obj:
			if not obj.primary_object in unique_recent_products_obj:
				unique_recent_products_obj.append(obj.primary_object)


	product_type = ContentType.objects.get_for_model(Product)
	popular_products_list = PageView.objects.filter(primary_content_type=product_type)\
	.values("primary_object_id")\
	.annotate(counter=Count("primary_object_id"))\
	.order_by("-counter")[:3]
	popular_products = []
	for item in popular_products_list:
		new_product = Product.objects.get(id=item['primary_object_id'])
		popular_products.append(new_product)
	print popular_products

	return render_to_response("home.html", locals(), context_instance=RequestContext(request))

def morerecents(request):
	if request.user.is_authenticated():
		all_recent_product_obj = request.user.pageview_set.get_products()[:10]
		unique_recent_products_obj = []
		for obj in all_recent_product_obj:
			if not obj.primary_object in unique_recent_products_obj:
				unique_recent_products_obj.append(obj.primary_object)
	else:
		all_recent_product_obj = PageView.objects.get_products()[:10]
		unique_recent_products_obj = []
		for obj in all_recent_product_obj:
			if not obj.primary_object in unique_recent_products_obj:
				unique_recent_products_obj.append(obj.primary_object)
	return render_to_response("allrecents.html", locals(), context_instance=RequestContext(request))
