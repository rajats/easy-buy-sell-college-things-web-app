
from django.shortcuts import render_to_response, RequestContext, Http404,HttpResponseRedirect
from analysis.signals import page_view

# Create your views here.

def home(request):
	viewall=False
	all_recent_product_obj = request.user.pageview_set.get_products()[:6]
	unique_recent_products_obj = []
	for obj in all_recent_product_obj:
		if not obj.primary_object in unique_recent_products_obj:
			unique_recent_products_obj.append(obj.primary_object)
	return render_to_response("home.html", locals(), context_instance=RequestContext(request))
