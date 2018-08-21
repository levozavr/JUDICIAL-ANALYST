from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^update$', views.upload_file),
    url(r'^$', views.search),
]