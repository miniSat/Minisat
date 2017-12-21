from django import forms
from .models import *

class compute_resource_form(forms.ModelForm):
    class Meta:
        model = compute_resource_model
        fields = '__all__'


class profile_form(forms.ModelForm):
    class Meta:
        model = profile_model
        fields = '__all__'
