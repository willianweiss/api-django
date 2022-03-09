# Generated by Django 3.0.6 on 2020-05-16 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configurations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=120)),
                ('message', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
