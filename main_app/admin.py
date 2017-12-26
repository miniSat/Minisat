from django.contrib import admin
from .models import compute_resource_model,profile_model,create_host_model,operating_system_model
# Register your models here.

admin.site.register(compute_resource_model)
admin.site.register(profile_model)
admin.site.register(create_host_model)
admin.site.register(operating_system_model)