from django.db import models

class Order(models.Model):
    client = models.ForeignKey('Client', related_name='orders', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255)
    amount = models.BigIntegerField()

    def __str__(self):
        return f"Order {self.id} - {self.client.name}"