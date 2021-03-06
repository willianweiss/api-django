# Generated by Django 3.0.1 on 2020-04-27 20:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('first_name', models.CharField(max_length=30, verbose_name='NOME')),
                ('last_name', models.CharField(max_length=30, verbose_name='SOBRENOME')),
                ('email', models.EmailField(help_text='Verifique os dados preenchidos', max_length=254, unique=True)),
                ('is_staff', models.BooleanField(default=False, verbose_name='STAFF')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='SUPER USER')),
                ('is_active', models.BooleanField(default=True, verbose_name='ATIVO')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='ÚLTIMO LOGIN')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='INSCRIÇÃO')),
                ('is_trusty', models.BooleanField(default=False, help_text='Designates whether this user has confirmed his account.', verbose_name='CONFIÁVEL?')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
            },
        ),
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100, unique=True, verbose_name='Chave')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('confirmed', models.BooleanField(blank=True, default=False, verbose_name='Confirmado?')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resets', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Nova Senha',
                'verbose_name_plural': 'Novas Senhas',
                'ordering': ['created_at'],
            },
        ),
    ]
