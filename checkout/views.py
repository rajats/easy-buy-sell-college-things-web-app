from django.shortcuts import render_to_response, RequestContext, Http404,HttpResponseRedirect
from django.contrib import messages    
from .models import Orders
from products.models import Product
from notifications.signals import notify
from notifications.models import NotifyUsers, Notification

# Create your views here.

def buy(request, slug):
	product = Product.objects.get(slug=slug)
	seller = product.user
	if request.user.is_authenticated():
		buyer = request.user
		order_obj = Orders.objects.create(buyer=request.user, seller=seller, product = product)
		notify.send(buyer, target = product, receiver_user=seller, msg='wants to buy', signal_sender=Orders)
	else:
		messages.warning(request, "Please login to buy this product!!")

	return render_to_response("checkout/buy.html", locals(), context_instance=RequestContext(request))
