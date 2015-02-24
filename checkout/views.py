from django.shortcuts import render_to_response, RequestContext, Http404,HttpResponseRedirect
from django.contrib import messages    
from .models import Checkout

# Create your views here.

def buy(request, slug):
	try:
		product = Product.objects.get(slug=slug)
	except:
		product = False
	seller = product.user
	if request.user.is_authenticated():
		buyer = request.user
		send_mail('test', 'new message test.', buyer.Email address, [seller.Email address], fail_silently=False)
	else:
		messages.warning(request, "Please login to buy this product!!")

	return render_to_response("checkout/buy.html", locals(), context_instance=RequestContext(request))
