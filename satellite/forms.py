from django import forms
from django.core.validators import RegexValidator


class Compute_resource_form(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'id': 'compute_name', "class": "form-control"}), label="Name", max_length=10)
    ip_address = forms.CharField(widget=forms.TextInput(attrs={'id': 'compute_ip', "class": "form-control"}), label="IP Address")
    root_password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'compute_password', "class": "form-control"}), label="Root Password", max_length=20)


class Profile_form(forms.Form):
    profile_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label="Profile Name", max_length=10)
    ram = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label="RAM(MB)", min_length=4, max_length=6, validators=[RegexValidator(r'^\d{1,10}$')])
    cpus = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label="CPUs", max_length=1, validators=[RegexValidator(r'^\d{1,10}$')])
    disk_size = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label="Disk Size(GB)", max_length=5, validators=[RegexValidator(r'^\d{1,10}$')])


class Create_host_form(forms.Form):
    vm_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label="Name")
    vm_os = forms.CharField(widget=forms.TextInput(attrs={'size': '25'}), label="Operating System")
    select_vm_profile = forms.CharField(widget=forms.TextInput(attrs={'size': '25'}), label="Profile")
    select_compute = forms.CharField(widget=forms.TextInput(attrs={'size': '25'}), label="Compute Resource")
    activation_name = forms.CharField(widget=forms.TextInput(attrs={'size': '25'}), label="Activation Name")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Root Password")
    select_host_group = forms.CharField(label="Host Group", widget=forms.TextInput(attrs={'size': '25'}))


class Operating_system_form(forms.Form):
    os_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label="Name", max_length=15)
    os_location = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label="Location", max_length=100)


class newContainerform(forms.Form):
    select_compute = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Compute", max_length=20)
    image_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Image Name", max_length=20)
    tag_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Tag", max_length=20, required=False)
    container_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Container Name", max_length=20, required=False)
    host_port = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Host Port'}), label="Ports", required=False)
    cont_port = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Container Port'}), required=False)


class Local_Images(forms.Form):
    select_compute = forms.CharField(widget=forms.TextInput(attrs={'size': '25'}), label="Compute", max_length=20)


class Product_form(forms.Form):
    product_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Name", max_length=20)
    product_location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="URL", max_length=100)


class View_form(forms.Form):
    view_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Name", max_length=20)
    select_product = forms.CharField(label="Select Products", max_length=20)


class Activation_form(forms.Form):
    activation_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Name', max_length=20)
    select_view = forms.CharField(label='Select Views', max_length=20)


class Host_group_form(forms.Form):
    host_group_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label="Name", max_length=20)
    select_compute = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id": "hs_compute"}), label="Select Compute", max_length=20)
    select_profile = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label="Select Profile", max_length=20)
    select_os = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label="Select Operating System", max_length=20)
    select_activation = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label="Select Activation Key", max_length=20)
