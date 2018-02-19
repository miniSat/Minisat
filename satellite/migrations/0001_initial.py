# Generated by Django 2.0 on 2018-02-18 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activation_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_name', models.CharField(max_length=20)),
                ('select_view', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Compute_resource_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True)),
                ('ip_address', models.CharField(max_length=15, unique=True)),
                ('root_password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Container_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('select_compute', models.CharField(max_length=20)),
                ('image_name', models.CharField(max_length=20, verbose_name='Image Name')),
                ('tag_name', models.CharField(max_length=20, verbose_name='Tag')),
                ('container_name', models.CharField(max_length=20, verbose_name='Container Name')),
                ('host_port', models.CharField(max_length=4)),
                ('cont_port', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Create_host_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vm_name', models.CharField(max_length=15)),
                ('vm_os', models.CharField(max_length=15)),
                ('select_vm_profile', models.CharField(max_length=10)),
                ('select_compute', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Operating_system_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('os_name', models.CharField(max_length=15)),
                ('os_location', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=20, verbose_name='Name')),
                ('product_location', models.CharField(max_length=100, verbose_name='Location')),
            ],
        ),
        migrations.CreateModel(
            name='Profile_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_name', models.CharField(max_length=10)),
                ('ram', models.IntegerField()),
                ('cpus', models.IntegerField()),
                ('disk_size', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='View_model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view_name', models.CharField(max_length=20)),
                ('select_product', models.CharField(max_length=20)),
            ],
        ),
    ]
