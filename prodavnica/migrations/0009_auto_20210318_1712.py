# Generated by Django 3.1.6 on 2021-03-18 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prodavnica', '0008_proizvod_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kupac',
            old_name='ime',
            new_name='username',
        ),
    ]