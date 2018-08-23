from django.db import models

# Create your models here.


class Document(models.Model):

    name = models.TextField(primary_key=True)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d', unique=True)

    def __str__(self):
        return 'Document: ' + self.name


class Json(models.Model):
    doc = models.OneToOneField(
        Document,
        on_delete=models.CASCADE,
    )

    text = models.TextField()

    def __str__(self):
        return 'Document: ' + self.doc.name
