from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(
        self, email, password, is_staff, is_superuser, **extra_fields
    ):
        # Create and save a User with the given email and password.
        now = timezone.now()
        if not email:
            raise ValueError("Você precisa de email para logar!")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields,
        )
        # TODO rever este save por causa do social login
        if password:
            user.set_password(password)

        if User.objects.filter(email=email).exists() and not password:
            get_user = User.objects.filter(email=email).first()
            return get_user
        else:
            user.save(using=self._db)
            return user

    def create_user(self, email, password=None, **extra_fields):
        # Create and save a regular User with the given email and password.
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        # Create and save a SuperUser with the given email and password.
        user = self._create_user(email, password, True, True, **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        "username",
        max_length=15,
        unique=True,
        help_text="15 caracteres ou menos: Letras, números e caracteres @ /. / + / - / _",  # noqa
    )
    first_name = models.CharField("NOME", max_length=30)
    last_name = models.CharField("SOBRENOME", max_length=30)
    fullname = models.CharField("NOME COMPLETO", max_length=30)
    email = models.EmailField(
        max_length=254, help_text="Verifique os dados preenchidos", unique=True
    )
    is_staff = models.BooleanField("STAFF", default=False)
    is_superuser = models.BooleanField("SUPER USER", default=False)
    is_active = models.BooleanField("ATIVO", default=True)
    last_login = models.DateTimeField("ÚLTIMO LOGIN", null=True, blank=True)
    date_joined = models.DateTimeField("INSCRIÇÃO", auto_now_add=True)
    is_trusty = models.BooleanField(
        "CONFIÁVEL?",
        default=False,
        help_text="Designates whether this user has confirmed his account.",
    )

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        # send_mail(subject, message, from_email, [self.email])
        pass

    def get_absolute_url(self):
        return f"/users/{self.pk}/"

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        return super(User, self).save(*args, **kwargs)


class PasswordReset(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Usuário",
        related_name="resets",
        on_delete=models.CASCADE,
    )
    key = models.CharField("Chave", max_length=100, unique=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    confirmed = models.BooleanField("Confirmado?", default=False, blank=True)

    def __str__(self):
        return f"{self.user} em {self.created_at}"

    class Meta:
        verbose_name = "Nova Senha"
        verbose_name_plural = "Novas Senhas"
        ordering = ["created_at"]
