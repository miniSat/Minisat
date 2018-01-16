from django.urls import (
    path)
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('compute_resource', views.compute_resource, name='compute_resource'),
    path('post_data', views.post_data, name='post_data'),
    path('profile', views.profile, name='profile'),
    path('post_profile', views.post_profile, name="post_profile"),
    path('create_host', views.create_host, name="create_host"),
    path('post_create_host', views.post_create_host, name="post_create_host"),
    path('operating_system', views.operating_system, name="operating_system"),
    path('post_operating_system', views.post_operating_system, name='post_operating_system'),
    path('new_container', views.new_container, name="new_container"),
    path('post_new_container', views.post_new_container, name='post_new_container'),
    path('local_images', views.local_images, name='local_images'),
    path('post_local_images', views.post_local_images, name="post_local_images" )
]
