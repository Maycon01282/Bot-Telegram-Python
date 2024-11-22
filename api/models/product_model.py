from django.db import models

class Product(models.Model):
    category = models.ForeignKey('Category', related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    photo = models.ImageField(upload_to='product_photos/', null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return self.name