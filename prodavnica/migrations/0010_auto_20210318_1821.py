# Generated by Django 3.1.6 on 2021-03-18 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('prodavnica', '0009_auto_20210318_1712'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kupac',
            options={},
        ),
        migrations.RenameField(
            model_name='kupac',
            old_name='username',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='kupac',
            name='korisnik',
        ),
        migrations.AddField(
            model_name='kupac',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='kupac',
            name='email',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
