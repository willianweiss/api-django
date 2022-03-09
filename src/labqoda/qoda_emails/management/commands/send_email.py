from django.conf import settings
from django.core.management.base import BaseCommand
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class Command(BaseCommand):
    help = "Migrate Users"

    def send_email(self):
        message = Mail(
            from_email="noreply.qoda@gmail.com",
            to_emails="andweber92@gmail.com",
            subject="Sending with Twilio SendGrid is Fun",
            html_content="<strong>and easy to do anywhere, even with Python</strong>",  # noqa
        )
        try:
            sg = SendGridAPIClient(settings.EMAIL_HOST_PASSWORD)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

    def handle(self, *args, **options):
        self.send_email()
        self.stdout.write(self.style.SUCCESS("Send Emails"))
