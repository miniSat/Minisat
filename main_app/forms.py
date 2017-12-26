from django import forms
from .models import *


class compute_resource_form(forms.ModelForm):
    class Meta:
        model = Compute_resource_model
        fields = '__all__'



class profile_form(forms.ModelForm):
    class Meta:
        model = Profile_model
        fields = '__all__'


class create_host_form(forms.ModelForm):
    class Meta:
        model = Create_host_model
        fields = '__all__'
