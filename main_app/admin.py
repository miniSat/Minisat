from django.contrib import admin

from .models import (
    Compute_resource_model,
    Create_host_model,
    Operating_system_model,
    Profile_model,
    Container_model,
    Local_image_model
)

# Register your models here.

admin.site.register(Compute_resource_model)
admin.site.register(Profile_model)
admin.site.register(Create_host_model)
admin.site.register(Operating_system_model)
admin.site.register(Container_model)
admin.site.register(Local_image_model)
