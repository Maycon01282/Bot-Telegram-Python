from django.db import models
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError

def validate_not_blank(value):
    if not value.strip():
        raise ValidationError('Fill in the name')

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
        validators=[validate_not_blank, MaxLengthValidator(255)],
        error_messages={
            'blank': 'Fill in the name',
            'max_length': 'Category name too long (more than 255 characters)'
        }
    )

    def __str__(self):
        return f"Category [id={self.id}, name={self.name}]"

    class Meta:
        db_table = 'categories'
