from django.db import models
from django.core.validators import MinValueValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _

class ProductCategory(models.Model):
    # Assuming Category model has at least a name field
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    photo_url = models.URLField(max_length=200, verbose_name=_("Photo URL"))
    name = models.CharField(
        max_length=255,
        validators=[
            MaxLengthValidator(255, message=_("Product name too long (more than 255 characters)"))
        ],
        verbose_name=_("Name")
    )
    description = models.TextField(
        max_length=2550,
        validators=[
            MaxLengthValidator(2550, message=_("Product description too long (more than 2550 characters)"))
        ],
        verbose_name=_("Description")
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(1, message=_("Minimum price is 1 $"))
        ],
        verbose_name=_("Price")
    )

    def __str__(self):
        return f"Product [id={self.id}, category={self.category}, photo_url={self.photo_url}, name={self.name}, description={self.description}, price={self.price}]"

    def __eq__(self, other):
        if isinstance(other, Product):
            return (
                self.id == other.id and
                self.category == other.category and
                self.photo_url == other.photo_url and
                self.name == other.name and
                self.description == other.description and
                self.price == other.price
            )
        return False

    def __hash__(self):
        return hash((self.id, self.category, self.photo_url, self.name, self.description, self.price))
