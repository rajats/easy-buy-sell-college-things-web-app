#serializers convert model data to json
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import routers, serializers, viewsets, permissions

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.contrib.auth.models import User

from .models import Product, ProductImage, ProductComments, Category

class ProductCommentsSerializer(serializers.HyperlinkedModelSerializer):
	#product_title = serializers.CharField(source='product.title', read_only=True)
	commenter = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
	#product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
	class Meta:
		model = ProductComments
		fields = [
			'url',
			'id',
			'comment',
			'pub_date',
			'commenter',
			#'product',
			#'product_title'
		]

class ProductCommentsViewSet(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]        #sessionauth will prevent login form pop up
	permission_classes = [permissions.IsAuthenticated, ]        #this ensures user is logged in while requesting
	queryset = ProductComments.objects.all()
	serializer_class = ProductCommentsSerializer

class ProductSerializer(serializers.HyperlinkedModelSerializer):
	productcomments_set = ProductCommentsSerializer(many=True, read_only=True)
	class Meta:
		model = Product
		fields = [
			'url',
			'id',
			'title',
			'description',
			'yearofpurchase',
			'price',
			'slug',
			'active',
			'ownercollege',
			'productcomments_set',
		]

class ProductViewSet(viewsets.ModelViewSet):
	authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]        #sessionauth will prevent login form pop up
	permission_classes = [permissions.IsAuthenticated, ]        #this ensures user is logged in while requesting
	queryset = Product.objects.all()
	serializer_class = ProductSerializer