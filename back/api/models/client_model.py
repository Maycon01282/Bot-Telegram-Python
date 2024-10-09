from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name