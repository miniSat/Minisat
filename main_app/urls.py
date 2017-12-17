from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('compute_resource', views.compute_resource, name='compute_resource')
]