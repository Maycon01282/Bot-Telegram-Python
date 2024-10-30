from django.db import models

class Order(models.Model):
    class Status(models.TextChoices):
        IN_PROCESS = 'in_process', 'In Process'
        SENT = 'sent', 'Sent'
        DELIVERED = 'delivered', 'Delivered'

    client = models.ForeignKey('Client', related_name='orders', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_PROCESS)
    amount = models.BigIntegerField()

    def __str__(self):
        return f"Order {self.id} - {self.client.name} - {self.get_status_display()}"