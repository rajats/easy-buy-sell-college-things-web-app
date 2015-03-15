from django.shortcuts import render_to_response, RequestContext, Http404,HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from products.models import Product
from .models import Cart, CartItem
from products.views import check_product
from checkout.models import Orders

# Create your views here.

def cart(request):
	try:
		cart_id = request.session['cart_id']
	except:
		cart_id = False
	if cart_id:
		cart = Cart.objects.get(id = cart_id)
	else:
		cart = False
	items = CartItem.objects.filter(cart = cart)
	if len(items) > 0:
		exists = True
	else:
		exists = False
	return render_to_response("cart/viewcart.html",locals(), context_instance=RequestContext(request))

def add_to_cart(request, id):
	try:
		product = Product.objects.get(id=id)
	except:
		product = False
	try:
		cart_id = request.session['cart_id']
	except:
		cart_id = False
	try:
		cart = Cart.objects.get(id = cart_id)
	except Cart.DoesNotExist:
		cart = Cart()
		cart.save()
		request.session['cart_id'] = cart.id
	if product:
		new_item, created = CartItem.objects.get_or_create(cart = cart, product = product)
		if created:
			new_item.cart = cart
			new_item.save()
			messages.success(request, 'added to cart')
		#else:
		#	new_item.delete()
		#	messages.success(request, 'removed from cart')
		return HttpResponseRedirect('/cart/')

def delete_from_cart(request, id):
	try:
		product = Product.objects.get(id=id)
	except:
		product = False
	try:
		cart_id = request.session['cart_id']
	except:
		cart_id = False
	try:
		cart = Cart.objects.get(id = cart_id)
	except Cart.DoesNotExist:
		messages.success(request, 'Nothing to remove')
	if product:
		new_item, created = CartItem.objects.get_or_create(cart = cart, product = product)
		new_item.delete()
	return HttpResponseRedirect('/cart/')


