from django.contrib import admin
from .models import UserProfile, UserOrderedProducts, UserSoldProducts

class UserOrderedProductsInline(admin.TabularInline):   
	model = UserOrderedProducts

class UserSoldProductsInline(admin.TabularInline):  
	model = UserSoldProducts

class UserProfileAdmin(admin.ModelAdmin):
	inlines = [UserOrderedProductsInline, UserSoldProductsInline] 
	class Meta:
		model = UserProfile

admin.site.register(UserProfile, UserProfileAdmin)
