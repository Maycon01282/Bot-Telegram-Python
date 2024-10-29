from django.contrib import admin
from api.models import *

admin.site.register(category_model.Category)
admin.site.register(product_model.Product)
admin.site.register(order_model.Order)
admin.site.register(order_item_model.OrderItem)
admin.site.register(client_model.Client)
admin.site.register(message_model.Message)
admin.site.register(user_model.User)
