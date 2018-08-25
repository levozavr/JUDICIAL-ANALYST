from django.db import models

# Create your models here.


class Document(models.Model):
    """
    model to save an document and use it again later
    """
    name = models.TextField(primary_key=True)
    docfile = models.FileField(upload_to='documents/', unique=True)

    def __str__(self):
        return 'Document: ' + self.name

