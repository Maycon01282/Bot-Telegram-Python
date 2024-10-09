from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name