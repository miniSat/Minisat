from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('compute_resource', views.compute_resource, name='compute_resource'),
    path('post_data', views.post_data, name='post_data'),
    path('profile',views.profile, name='profile'),
    path('post_profile',views.post_profile,name="post_profile"),

]