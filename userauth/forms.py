from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)

class RegistrationForm(forms.Form):
	username = forms.CharField()
	email = forms.EmailField()
	password = forms.CharField(widget = forms.PasswordInput)
	password1 = forms.CharField(widget = forms.PasswordInput)

	def clean_username(self):
		username = self.cleaned_data['username']
		if User.objects.filter(username = username).exists():
			raise forms.ValidationError("username %s already exists" %(username))
		return username

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email = email).exists():
			raise forms.ValidationError("email %s already exists" %(email))
		return email

	def clean(self):
		cleaned_data = super(RegistrationForm,self).clean()
		password = cleaned_data.get("password")
		password1 = cleaned_data.get("password1")
		if password != password1:
			raise forms.ValidationError("Passwords do not match")
			del cleaned_data['password']
			del cleaned_data['password1']
		else:
			set_password = make_password(password)
			cleaned_data['password'] = set_password
			cleaned_data['password1'] = set_password
		return cleaned_data




