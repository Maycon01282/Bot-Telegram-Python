from django.db import models

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=255, null=False)
    text = models.TextField(max_length=4096, null=False)

    def __str__(self):
        return f"Message [id={self.id}, name={self.name}, description={self.description}, text={self.text}]"

    def __eq__(self, other):
        if isinstance(other, Message):
            return (self.id == other.id and
                    self.name == other.name and
                    self.description == other.description and
                    self.text == other.text)
        return False

    def __hash__(self):
        return hash((self.id, self.name, self.description, self.text))
