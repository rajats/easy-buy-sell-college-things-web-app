import json

from django.http import HttpResponse
from django.shortcuts import render_to_response, RequestContext, Http404,HttpResponseRedirect
from django.contrib import messages    
from django.contrib.auth.decorators import login_required

from .models import Orders
from products.models import Product
from notifications.signals import notify
from notifications.models import NotifyUsers, Notification

@login_required
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

@login_required
def confirmorder(request, slug):
	product = Product.objects.get(slug=slug)
	order = Orders.objects.get(product=product)
	order.confirmed = True
	order.save()
	seller = order.seller
	buyer = order.buyer
	notify.send(seller, target = product, receiver_user=buyer, msg='with email %s and phone %s confirmed your order for'% (seller.email,product.ownerphone) , signal_sender=Orders)
	return HttpResponseRedirect('/products/%s' % product.slug)

@login_required
def rejectorder(request, slug):
	product = Product.objects.get(slug=slug)
	order = Orders.objects.get(product=product)
	order.rejected = True
	order.save()
	return HttpResponseRedirect('/products/%s' % product.slug)
