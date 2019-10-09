from django.urls import (
    path)
from . import views

# We need to import our app's views to call our home views,compute views etc.

urlpatterns = [
    path('', views.home, name='home'),
    # First paramter:localhost:8000 , Second paramter:Look inside the views.py file Call the home view fuction
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
    path('post_local_images', views.post_local_images, name="post_local_images"),
    path('<slug:cname>/<slug:vm_id>', views.vm_info, name='vm_info'),
    path('get_virtual_mc', views.get_virtual_mc, name='get_virtual_mc'),
    path('get_running_containers', views.get_running_containers, name='get_running_containers'),
    path('vm_start', views.vm_start, name='vm_start'),
    path('vm_pause', views.vm_pause, name='vm_pause'),
    path('containers/start_container/', views.start_container, name="start_container"),
    path('containers/pause_container/', views.stop_container, name="stop_container"),
    path('product', views.product, name="product"),
    path('post_product', views.post_product, name='post_product'),
    path('delete', views.delete, name="delete"),
    path('view', views.content_view, name='content_view'),
    path('post_content_view', views.post_content_view, name="post_content_view"),
    path('activation', views.activation_view, name='activation_view'),
    path('post_activation_view', views.post_activation_view, name='post_activation_view'),
]
