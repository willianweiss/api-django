import structlog
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.defaultfilters import striptags
from django.template.loader import render_to_string

logger = structlog.get_logger(__name__)


def send_mail_contact(instance, default_emails):
    logger.info(f"Enviando email para: {default_emails}")
    message = (
        f"Nome: {instance.name} \n"
        f"Email: {instance.email} \n"
        f"Mensagem: {instance.message} \n"
    )

    email = EmailMessage("Contato Recebido", message, to=default_emails)
    email.send()


def send_mail_template(
    subject,
    template_name,
    context,
    recipient_list,
    from_email=settings.DEFAULT_FROM_EMAIL,
    fail_silently=False,
):
    message_html = render_to_string(template_name, context)
    message_text = striptags(message_html)
    email = EmailMultiAlternatives(
        subject=subject,
        body=message_text,
        from_email=from_email,
        to=recipient_list,
    )
    email.attach_alternative(message_html, "text/html")
    email.send(fail_silently=fail_silently)
