from django.conf import settings
from django.db import models

from labqoda.helpers.email.base import send_mail_contact


class DefaultInstructor(models.Model):

    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Instrutor Padrão das aulas"
        verbose_name_plural = "Instrutor Padrão das aulas"

    def __str__(self):
        return f"{self.instructor}"


class DefaultContactEmail(models.Model):

    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Email que receberá mensagens de contato."
        verbose_name_plural = "Emails que receberão mensagens de contato."

    def __str__(self):
        return f"{self.email}"


class Contact(models.Model):

    name = models.CharField(max_length=120, verbose_name="nome")
    email = models.EmailField(max_length=120, verbose_name="email")
    message = models.TextField(verbose_name="mensagem")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pagina de Contato"
        verbose_name_plural = "Pagina de Contatos"

    def __str__(self):
        return f"nome: {self.name}"


def post_save_contact(created, instance, **kwargs):
    if created:
        default_emails = DefaultContactEmail.objects.all().values_list(
            "email", flat=True
        )
        if default_emails:
            send_mail_contact(instance, default_emails)


models.signals.post_save.connect(
    post_save_contact, sender=Contact, dispatch_uid="post_save_contact"
)
