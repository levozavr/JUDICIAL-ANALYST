from django.contrib import admin

# Register your models here.
from analitics.models import Document, Json

admin.site.register(Document)
admin.site.register(Json)