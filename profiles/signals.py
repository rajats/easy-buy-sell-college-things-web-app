from django.dispatch import Signal

update_total_products = Signal(providing_args=[])
new_user_profile = Signal(providing_args=[])
update_total_orders = Signal(providing_args=['ordered_product',])
update_total_sold_products = Signal(providing_args=['sold_product',])