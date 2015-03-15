import json

from itertools import chain
import itertools

from django.http import HttpResponse
from django.shortcuts import render_to_response, RequestContext, Http404,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify
from django.forms.models import modelformset_factory
from django.core.urlresolvers import reverse
from django.db.models import Q 
from django.utils import timezone
from django.contrib import messages 

from endless_pagination.decorators import page_template   
from .models import Product, Category, ProductImage, ProductComment
from .forms import ProductForm, ProductImageForm, ProductCommentForm, UnRegUserProductCommentForm
from cart.models import Cart
from analysis.signals import page_view
from analysis.models import PageView
from notifications.signals import notify
from notifications.models import NotifyUsers, Notification
from checkout.models import Orders


from django.core.mail import send_mail

# Create your views here.

def check_product(user, product):
    if product in request.user.userpurchase.products.all():
        return True
    else:
        return False


"""
def list_all(request):
    products = Product.objects.filter(active=True)
    if request.user.is_authenticated():
        products = Product.objects.filter(active=True).filter(~Q(user = request.user))
    return render_to_response("products/all.html", locals(), context_instance=RequestContext(request))
"""

@page_template('products/all_index_page.html')
def list_all(request,template='products/all_index.html', extra_context=None):
    products = Product.objects.filter(active=True)
    if request.user.is_authenticated():
        products = Product.objects.filter(active=True).filter(~Q(user = request.user))

    context = {
        'products': products,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))
def single(request, slug):
    #send_mail('test', 'new message test.', 'rajat11ukawa@gmail.com', ['rajatk@outlook.in'], fail_silently=False)
    product = Product.objects.get(slug=slug)
    active = product.active
    if not active:
        messages.warning(request, 'This product is currently sold out')
    images = ProductImage.objects.filter(product=product)
    categories = product.category_set.all()
    page_view.send(request.user, page_path = request.get_full_path(),primary_obj = product)
    #print request.user.userpurchase.products.all()
    categories = product.category_set.all()
    if request.user == product.user:
        edit = True
    else:
        edit = False
    related = []
    if len(categories) >= 1:
        for category in categories:
            products_category = category.product.all()
            for item in products_category:
                if not item == product:
                    related.append(item)

    try:
        ordered_products = []
        if request.user.is_authenticated():
            user_orders = Orders.objects.filter(buyer = request.user)
            for order_obj in user_orders:
                ordered_products.append(order_obj.product)

        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id = cart_id)
        for item in cart.cartitem_set.all():
            if item.product == product:
                in_cart = True

    except:
        in_cart = False

    return render_to_response("products/single.html", locals(), context_instance=RequestContext(request))

def edit_product(request, slug):
    instance = Product.objects.get(slug=slug)
    if request.user == instance.user:
        form = ProductForm(request.POST or None, instance = instance)
        if form.is_valid():
            product_edit = form.save(commit=False)
            product_edit.save()
        return render_to_response("products/edit.html", locals(), context_instance=RequestContext(request))
    else:
        raise Http404

def mark_product_as_sold(request, slug):
    instance = Product.objects.get(slug=slug)
    if request.user == instance.user:
        instance.active = False
        instance.save()
    return HttpResponseRedirect('/products/')


def add_product(request):
    if request.user.is_authenticated():
        form = ProductForm(request.POST or None)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.active = True
            product.slug = temp = slugify(form.cleaned_data['title'])   #automatically creates slug using title


            for x in itertools.count(1):
                if not Product.objects.filter(slug=product.slug).exists():
                    break
                product.slug = '%s-%d' % (temp, x)


            product.save()
            return HttpResponseRedirect('/products/%s/images/' %(product.slug))
        return render_to_response("products/edit.html", locals(), context_instance=RequestContext(request))
    else:
        raise Http404

def manage_product_image(request, slug):
    try:
        product = Product.objects.get(slug = slug)
    except:
        product = False
    if request.user == product.user:
        queryset = ProductImage.objects.filter(product__slug=slug)
        ProductImageFormset = modelformset_factory(ProductImage, form = ProductImageForm,)  # can_delete = True
        formset = ProductImageFormset(request.POST or None, request.FILES or None,queryset = queryset)   #depending on foreignkey
        form = ProductImageForm(request.POST or None)
        if formset.is_valid():
            for form in formset:
                instance = form.save(commit = False)
                instance.product = product
                instance.save();
            if formset.deleted_forms:
                formset.save()
        return render_to_response("products/manage_images.html", locals(), context_instance=RequestContext(request))
    else:
        raise Http404

def search(request):
    try:
        q = request.GET.get('q', '')
    except:
        q = False
    if q:
        query = q
    products_set = Product.objects.filter(										#searching thru products and categories
        Q(title__icontains = q)|
        Q(description__icontains=q)
    )
    category_set = Category.objects.filter(										#searching thru products and categories
        Q(title__icontains = q)|
        Q(description__icontains=q)
    )
    products = list(chain(products_set, category_set))

    return render_to_response("products/search.html", locals(), context_instance=RequestContext(request))

def user_products(request):
    products = Product.objects.filter(user = request.user)
    return render_to_response("products/all.html", locals(), context_instance=RequestContext(request))

def add_comment(request, slug):
    prod=Product.objects.get(slug=slug)    
    if request.method=='POST':
        cform=ProductCommentForm(request.POST)         #create commentform using POST
        if cform.is_valid():
            comment_text = cform.cleaned_data['comment']
            new_comment = ProductComment.objects.create(product=prod,commenter=request.user,comment=comment_text,pub_date=timezone.now())
            messages.success(request, "Your comment was added")
            sent_senders=[]
            if NotifyUsers.objects.filter(product = prod).exists():
                for obj in NotifyUsers.objects.filter(product = prod):
                    if request.user != obj.sender:
                        if obj.sender not in sent_senders:
                            notify.send(request.user, action=new_comment, target = prod, receiver_user=obj.sender, msg='commented on', signal_sender=Product) 
                    sent_senders.append(obj.sender)
            else:
                notify.send(request.user, action=new_comment, target = prod, receiver_user=prod.user, msg='commented on', signal_sender=Product)
        else:
            messages.error(request, "There was an error with your comment")

            return HttpResponseRedirect('/products/%s/' %(prod.slug)) 
    else:
        cform=ProductCommentForm()              
    return render_to_response("products/add_comment.html", locals(), context_instance=RequestContext(request))


@page_template('products/all_index_page.html')
def category_products(request, catslug, template='products/all_index.html', extra_context=None):
    category = Category.objects.get(slug=catslug)
    products = Product.objects.filter(category=category,active=True)
    if request.user.is_authenticated():
        products = Product.objects.filter(category=category,active=True).filter(~Q(user = request.user))
    context = {
        'products': products,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(template, context, context_instance=RequestContext(request))



def get_products_categories_using_ajax(request):                                       #return HttpResponse with ajax data
    if request.is_ajax() and request.method == "POST":
        categories=["all"]
        category_slugs=["products"]
        try:
            categories_obj = Category.objects.all()
        except Category.DoesNotExist:
            categories_obj = None
        for obj in categories_obj:
            categories.append(obj.title)
            category_slugs.append(obj.slug)
        data = {
            "categories": categories,
            "category_slugs": category_slugs,
        }
        json_data = json.dumps(data)               #converts to json
        print categories 
        return HttpResponse(json_data, content_type='application/json')
    else:
        raise Http404


