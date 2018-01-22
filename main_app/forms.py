from django import forms


class Compute_resource_form(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), label="Name", max_length=10)
    ip_address = forms.CharField(widget=forms.TextInput(attrs={'size': '50', 'id': 'ip_add'}), label="IP Address")
    root_password = forms.CharField(widget=forms.PasswordInput(attrs={'size': '50'}), label="Root Password",
                                    max_length=20)


class Profile_form(forms.Form):
    profile_name = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), label="Profile Name", max_length=10)
    ram = forms.IntegerField(label="RAM(MB)")
    cpus = forms.IntegerField(label="CPUs")
    disk_size = forms.IntegerField(label="Disk Size(GB)")


class Create_host_form(forms.Form):
    vm_name = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), label="VM Name")
    vm_os = forms.CharField(widget=forms.TextInput(attrs={'size': '25'}), label="VM OS")
    select_vm_profile = forms.CharField(widget=forms.TextInput(attrs={'size': '25'}), label="VM Profile")
    select_compute = forms.CharField(widget=forms.TextInput(attrs={'size': '25'}), label="Compute")


class Operating_system_form(forms.Form):
    os_name = forms.CharField(label="Name", max_length=15)
    os_location = forms.CharField(label="Location", max_length=100)


class newContainerform(forms.Form):
    select_compute = forms.CharField(label="Compute", max_length=20)
    image_name = forms.CharField(label="Image Name", max_length=20)
    tag_name = forms.CharField(label="Tag", max_length=20)
    container_name = forms.CharField(label="Container Name", max_length=20)
    command = forms.CharField(label="Command", max_length=15)
    entry_point = forms.CharField(label="Entry Point", max_length=15)


class Local_Images(forms.Form):
    select_compute = forms.CharField(label="Compute", max_length=20)
