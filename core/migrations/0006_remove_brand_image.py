# Generated by Django 4.2 on 2024-05-27 01:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_brand_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='image',
        ),
    ]
