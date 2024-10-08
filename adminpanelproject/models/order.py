from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

class OrderClient(models.Model):
    # Define the Client model fields here
    pass

class OrderStatus(models.TextChoices):
    # Define the OrderStatus choices here
    PENDING = 'PENDING', 'Pending'
    COMPLETED = 'COMPLETED', 'Completed'
    # Add other statuses as needed

class Order(models.Model):
    client = models.OneToOneField(OrderClient, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    amount = models.PositiveBigIntegerField(validators=[MinValueValidator(1, message="Minimum amount is 1 $")])

    def __str__(self):
        return f"Order [id={self.id}, client={self.client}, created_date={self.created_date}, status={self.status}, amount={self.amount}]"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    # Define other fields for OrderItem here
    pass
