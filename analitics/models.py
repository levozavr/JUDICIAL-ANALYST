from django.db import models

# Create your models here.


class Document(models.Model):

    name = models.CharField(max_length=256)
    analised_information = models.CharField(max_length=2048)
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')


    def __str__(self):
        return 'Document: ' + self.name