
from django.shortcuts import render_to_response, RequestContext, Http404,HttpResponseRedirect

# Create your views here.

def home(request):
	return render_to_response("home.html", locals(), context_instance=RequestContext(request))
