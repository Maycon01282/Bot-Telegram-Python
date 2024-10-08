from django.db import models

class OrderItemOrder(models.Model):
    # Define fields for Order model
    pass

class OrderItemProduct(models.Model):
    # Define fields for Product model
    pass

class OrderItemDetails(models.Model):
    order = models.ForeignKey(OrderItemOrder, on_delete=models.CASCADE, related_name='order_items')
    product = models.OneToOneField(OrderItemProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_name = models.CharField(max_length=255)
    product_price = models.BigIntegerField()

    def get_total_price(self):
        return self.quantity * self.product_price

    def __str__(self):
        return f"OrderItem [id={self.id}, order={self.order}, product={self.product}, quantity={self.quantity}, product_name={self.product_name}, product_price={self.product_price}]"

    def __eq__(self, other):
        if isinstance(other, OrderItemDetails):
            return (self.id == other.id and
                    self.order == other.order and
                    self.product == other.product and
                    self.quantity == other.quantity and
                    self.product_name == other.product_name and
                    self.product_price == other.product_price)
        return False

    def __hash__(self):
        return hash((self.id, self.order, self.product, self.quantity, self.product_name, self.product_price))
