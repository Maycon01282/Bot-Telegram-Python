from django.db import models
from django.core.validators import MaxLengthValidator

class Client(models.Model):
    id = models.AutoField(primary_key=True)
    chat_id = models.BigIntegerField(unique=True, null=False)
    name = models.CharField(max_length=255, validators=[MaxLengthValidator(255, message="Name too long (more than 255 characters)")], blank=True, null=True)
    phone_number = models.CharField(max_length=255, validators=[MaxLengthValidator(255, message="Phone number too long (more than 255 characters)")], blank=True, null=True)
    city = models.CharField(max_length=255, validators=[MaxLengthValidator(255, message="City too long (more than 255 characters)")], blank=True, null=True)
    address = models.CharField(max_length=255, validators=[MaxLengthValidator(255, message="Address too long (more than 255 characters)")], blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Client [id={self.id}, chat_id={self.chat_id}, name={self.name}, phone_number={self.phone_number}, city={self.city}, address={self.address}, active={self.is_active}]"

    def __eq__(self, other):
        if isinstance(other, Client):
            return (
                self.id == other.id and
                self.chat_id == other.chat_id and
                self.name == other.name and
                self.phone_number == other.phone_number and
                self.city == other.city and
                self.address == other.address and
                self.is_active == other.is_active
            )
        return False

    def __hash__(self):
        return hash((self.id, self.chat_id, self.name, self.phone_number, self.city, self.address, self.is_active))
