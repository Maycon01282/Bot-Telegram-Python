from django.db import models

class OrderItem(models.Model):
    order = models.ForeignKey('Order', related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', related_name='order_items', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product} in order {self.order.id}"