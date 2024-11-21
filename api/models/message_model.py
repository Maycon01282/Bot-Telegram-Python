from django.db import models
from api.models.client_model import Client  # Assuming the Client model is defined elsewhere

class Message(models.Model):
    content = models.CharField(max_length=255)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=1)  # Set default Client ID
    name = models.CharField(max_length=100)
    description = models.TextField()
    text = models.TextField()

    def __str__(self):
        return self.name