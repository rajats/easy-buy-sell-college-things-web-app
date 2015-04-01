from django.contrib import admin
from .models import UserProfile, UserOrderedProducts

class UserOrderedProductsInline(admin.TabularInline):   
	model = UserOrderedProducts

class UserProfileAdmin(admin.ModelAdmin):
	inlines = [UserOrderedProductsInline] 
	class Meta:
		model = UserProfile

admin.site.register(UserProfile, UserProfileAdmin)
