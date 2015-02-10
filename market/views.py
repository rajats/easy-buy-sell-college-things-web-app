
from django.shortcuts import render_to_response, RequestContext, Http404,HttpResponseRedirect
from analysis.signals import page_view

# Create your views here.

def home(request):
	#page_view.send(
	#	request.user,
	#	page_path=request.get_full_path(),
	#	)
	return render_to_response("home.html", locals(), context_instance=RequestContext(request))
