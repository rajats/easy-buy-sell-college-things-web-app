from django.shortcuts import render, HttpResponseRedirect
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages


User = get_user_model()

# Create your views here.
def signin(request):
	form = LoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username = username, password = password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect('/products/')
		else:
			return HttpResponseRedirect('/userauth/register/')
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
	context = {'form': form}
	return render(request, "userauth/form.html",context)

def signout(request):
	logout(request)
	messages.success(request,"You have logged out")
	return HttpResponseRedirect('/userauth/login/')

