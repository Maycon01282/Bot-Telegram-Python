from django.db import models

class Order(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'New'
        IN_PROCESS = 'in_process', 'In Process'
        SENT = 'sent', 'Sent'
        DELIVERED = 'delivered', 'Delivered'
        
    class PaymentMethod(models.TextChoices):
        PIX = 'pix', 'Pix'
        CASH_ON_DELIVERY = 'cash_on_delivery', 'Cash on Delivery'

    client = models.ForeignKey('Client', related_name='orders', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_PROCESS)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH_ON_DELIVERY)
    amount = models.BigIntegerField()

    def __str__(self):
        return f"Order {self.id} - {self.client.name} - {self.get_status_display()}"