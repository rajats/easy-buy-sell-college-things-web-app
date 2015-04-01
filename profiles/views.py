from django.shortcuts import render_to_response, RequestContext, Http404,HttpResponseRedirect

from products.models import Product
from .models import UserProfile, UserOrderedProducts

def library(request):
	if request.user.is_authenticated():
		profile = UserProfile.objects.get(user=request.user)
		orders = UserOrderedProducts.objects.filter(profile=profile)
		return render_to_response("profiles/profile.html", locals(), context_instance=RequestContext(request))
	else:
		return Http404
