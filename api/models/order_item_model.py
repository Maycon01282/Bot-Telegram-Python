from django.db import models
from api.models.order_model import Order  # Import the Order class

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', related_name='order_items', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add a default value for 'price'

    def __str__(self):
        return f"{self.quantity} of {self.product} in order {self.order.id}"