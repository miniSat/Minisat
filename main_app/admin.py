from django.contrib import admin
from .models import compute_resource_model,profile_model
# Register your models here.

admin.site.register(compute_resource_model)
admin.site.register(profile_model)