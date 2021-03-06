# Generated by Django 3.0.1 on 2020-04-27 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('certificates', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pathcertificate',
            name='path',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Path'),
        ),
        migrations.AddField(
            model_name='coursecertificate',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course'),
        ),
    ]
