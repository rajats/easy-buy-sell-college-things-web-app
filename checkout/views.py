import json
from django.http import HttpResponse

from django.shortcuts import render_to_response, RequestContext, Http404,HttpResponseRedirect
from django.contrib import messages    
from .models import Orders
from products.models import Product
from notifications.signals import notify
from notifications.models import NotifyUsers, Notification

# Create your views here.

'''def buy(request, slug):
	product = Product.objects.get(slug=slug)
	seller = product.user
	if request.user.is_authenticated():
		buyer = request.user
		order_obj = Orders.objects.create(buyer=request.user, seller=seller, product = product)
		notify.send(buyer, target = product, receiver_user=seller, msg='wants to buy', signal_sender=Orders)
		user_orders = Orders.objects.filter(buyer = request.user)
	else:
		messages.warning(request, "Please login to buy this product!!")
		user_orders = []

	return render_to_response("checkout/buy.html", locals(), context_instance=RequestContext(request))
'''

def buy(request, slug):
	if request.is_ajax() and request.method == "POST":
		product = Product.objects.get(slug=slug)
		seller = product.user
		ordered = 0
		if request.user.is_authenticated():
			buyer = request.user
			order_obj = Orders.objects.create(buyer=request.user, seller=seller, product = product)
			notify.send(buyer, target = product, receiver_user=seller, msg='wants to buy', signal_sender=Orders)
			ordered = 1
		else:
			pass
		data = {
			"ordered": ordered,
		}
		json_data = json.dumps(data)               #converts to json 
		return HttpResponse(json_data, content_type='application/json')
	else:
		raise Http404
