import json
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, RequestContext, Http404,HttpResponseRedirect

from .models import Notification, NotifyUsers
from products.models import Category
# Create your views here.

@login_required
def all(request):
	all_notify_obj = NotifyUsers.objects.filter(user = request.user)
	notifications=[]
	for obj in all_notify_obj:
		notifications.append(obj.notifications)
	
	return render_to_response("notifications/all.html", locals(), context_instance=RequestContext(request))



@login_required
def get_notifications_using_ajax(request):                                       #return HttpResponse with ajax data
	if request.is_ajax() and request.method == "POST":
		all_notify_obj = NotifyUsers.objects.filter(user = request.user)
		notifications=[]
		for obj in all_notify_obj:
			notifications.append(obj.notifications)
		count = 0
		notes = []
		for note in notifications:
			if not note.read:
				notes.append(str(note.get_link()))
				count += 1
		data = {
			"notifications": notes,
			"count": count,
		}
		json_data = json.dumps(data)               #converts to json 
		return HttpResponse(json_data, content_type='application/json')
	else:
		raise Http404

@login_required
def mark_all_as_read(request):                                       #return HttpResponse with ajax data
	if request.is_ajax() and request.method == "POST":
		all_notify_obj = NotifyUsers.objects.filter(user = request.user)
		notifications=[]
		for obj in all_notify_obj:
			notifications.append(obj.notifications)
		notes = []
		test=2
		for note in notifications:
			note.read=True
			note.save()
		data = {
			"notifications": notes,
		}
		json_data = json.dumps(data)               #converts to json 
		return HttpResponse(json_data, content_type='application/json')
	else:
		raise Http404



