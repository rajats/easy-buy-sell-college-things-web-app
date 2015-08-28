from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from .forms import LoginForm, RegistrationForm
from profiles.signals import new_user_profile

User = get_user_model()

def signin(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('home'))
	form = LoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username = username, password = password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect('/products/')
		else:
			messages.error(request, 'username or password does not match')
	context = {'form': form}
	return render(request, "userauth/form.html",context)

def register(request):
	form = RegistrationForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data['username']
		email = form.cleaned_data['email']
		password = form.cleaned_data['password']
		new_user, created = User.objects.get_or_create(username = username, email = email)
		if created:
			new_user.password = password
			new_user.save()
			new_user_profile.send(new_user)
			messages.success(request, 'Your account has been registered, You can login now!')
			return HttpResponseRedirect('/userauth/login/')
	context = {'form': form}
	return render(request, "userauth/form.html",context)

def signout(request):
	logout(request)
	messages.success(request,"You have logged out")
	return HttpResponseRedirect('/userauth/login/')

