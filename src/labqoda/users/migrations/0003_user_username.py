# Generated by Django 3.0.5 on 2020-05-02 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_fullname'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='xxx', help_text='15 caracteres ou menos: Letras, números e caracteres @ /. / + / - / _', max_length=15, unique=True, verbose_name='username'),
            preserve_default=False,
        ),
    ]
