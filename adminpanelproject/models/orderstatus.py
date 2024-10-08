from django.db import models

class OrderStatus(models.TextChoices):
    WAITING = 'Waiting', 'Waiting'
    PROCESSED = 'Processed', 'Processed'
    COMPLETED = 'Completed', 'Completed'
    CANCELED = 'Canceled', 'Canceled'
