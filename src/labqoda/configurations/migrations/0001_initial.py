# Generated by Django 3.0.6 on 2020-05-16 20:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultContactEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Email que receberá mensagens de contato.',
                'verbose_name_plural': 'Emails que receberão mensagens de contato.',
            },
        ),
        migrations.CreateModel(
            name='DefaultInstructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Instrutor Padrão das aulas',
                'verbose_name_plural': 'Instrutor Padrão das aulas',
            },
        ),
    ]
