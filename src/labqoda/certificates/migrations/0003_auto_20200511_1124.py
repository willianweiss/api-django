# Generated by Django 3.0.6 on 2020-05-11 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0002_auto_20200427_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursecertificate',
            name='public',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pathcertificate',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
