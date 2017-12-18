from django.contrib import admin
from .models import compute_resource,profile
# Register your models here.

admin.site.register(compute_resource)
admin.site.register(profile)