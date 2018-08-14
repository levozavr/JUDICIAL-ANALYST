from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^analitics', views.upload_file, name='index'),
]