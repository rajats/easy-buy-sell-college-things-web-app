# easy-buy-sell-college-things-web-app
easy buy/sell college things web app is implemented as part as part of my sixth semester college project.We will be using django web application 
framework and postgresql as database.

For screenshots of project please visit:
[Screenshots](https://drive.google.com/folderview?id=0B298A8MGFMjKfnhidTJwd24yNm5ncVlIcXhxa2xlOGtjMkNJR2loSF96SFlqeWEtQTZfcG8&usp=sharing)

The purpose of this project is to allow college students to get college needed things easily at lesser price.Students can search 
if a product is available in products library and
if avialable they can check if it is available in their college.

All registered user will have the facility to add a new product.
Since a product may receive more than one buy request, we are giving buyer, the power to mark a product as sold.
Sold product cannot be added to the cart.
If the user is interested in buying things, checkout app will send notification to the product's owner(seller) about buyer's interest in buying the
product.Now, it is upto seller of product to sell that product to buyer.A buy request will be created and the seller will be notfied about that.
A buy request will have three options for the seller:

1) *confirm order*,

2) *reject order*,

3) *save for later*,

if the seller clicks on confirm order then the buyer will be notified about the order confirmation and seller contact details will be shared with
 the buyer,
if the seller clicks on reject order then the buy request will be removed and the buyer will not be notified about this rejection,
if the seller clicks on save for later then the buy request will still be present in buy requests panel unless seller confirms or rejects order.

The web app will allow guest users to browse through products library but for buying, users have to register themselves.

Home page will feature recently searched products and top popular products.

##The project easybuy is divided in 6 django apps.
##1) Product:
This app deals with all product related things like searching a product,adding a product,viewing a single product or viewing all products, editing
 a product, marking a product as sold, adding comment on a product.
Viewing all products and viewing all products in a category has twitter style pagination using ajax.

##2) Cart:
This app deals with viewing the cart, adding a product in the cart, deleting a product from the cart.We are using session to keep product in cart.

##3) Notifications:
This app deals with making a notification.We have a notify signal which has sender, receiver, action, target, message, signal sender(from which 
model signal came),read , timestamp as its attributes.We are using ContentType for sender, signal sender, action, target. Content type will allow us
to send signal from any model. This app allows user to view all notifications so far, see only new new notfications in notification dropdown using ajax, and
 mark all notfications as read.If all notifications are read then notification dropdown will have link to view all notifications.
 
##4) Checkout:
This app takes care of everything after a user(buyer) creates a buy request.Once a buy request is created a notfication is send to the seller about buy request.
This app has functionality of confirming a order and rejecting a order for the seller.

##5) Userauth:
This app allows a user to register themselves at site.It has functionality of signing in a registered user, signing out a registered user and registering 
a new user at site.

##6) Analysis:
Here also we are using django signals for getting recently searched products.A custom signal pageview is used.Everytime when a product is viewed a 
pageview signal is send from product app and this creates a pageview object which has path to viewed product.Every pageview has a user if the user is registered.
So, for a registered user we are showing products recently searched by the user and for guest user we are showing all recently searched products from all users.
For getting top popular products we are using django aggregation, so product which has most pageviews is popular. 
