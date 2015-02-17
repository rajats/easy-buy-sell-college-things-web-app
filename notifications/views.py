import json
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, RequestContext, Http404,HttpResponseRedirect

from .models import Notification
# Create your views here.

@login_required
def all(request):
	notifications = Notification.objects.all_for_user(request.user)
	
	return render_to_response("notifications/all.html", locals(), context_instance=RequestContext(request))



@login_required
def get_notifications_using_ajax(request):                                       #return HttpResponse with ajax data
	if request.is_ajax() and request.method == "POST":
		notifications = Notification.objects.all_for_user(request.user)
		count = notifications.count()
		notes = []
		for note in notifications:
			notes.append(str(note.get_link()))
		data = {
			"notifications": notes,
			"count": count,
		}
		json_data = json.dumps(data)               #converts to json 
		return HttpResponse(json_data, content_type='application/json')
	else:
		raise Http404