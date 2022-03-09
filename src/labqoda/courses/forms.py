import uuid

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from labqoda.helpers.email.base import send_mail_template

from .models import Course, Module, Video
from .services.vdocipher import VdoCipher


class VideoUploadForm(ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = Video
        fields = ["id", "videoid", "order"]

    def clean(self):
        if "file" in self.changed_data:
            credentials, _ = self.upload_file(self.cleaned_data)
            videoid = credentials.get("videoId")
            self.cleaned_data["videoid"] = videoid

    def upload_file(self, data):
        vdochiper = VdoCipher()

        title = uuid.uuid4()
        video_file = data.get("file")

        try:
            credentials = vdochiper.make_credentials(title)
            file_result = vdochiper.upload_file(credentials, video_file)
            return credentials, file_result
        except Exception as err:
            raise ValidationError({"file": err.args[0]})

    def save(self, commit=True):
        return super(VideoUploadForm, self).save(commit=commit)


class Contato(forms.Form):
    nome = forms.CharField(label="Nome", max_length=100)
    email = forms.EmailField(label="Email")
    msg = forms.CharField(label="Mensagem/Dúvida", widget=forms.Textarea)

    def send_mail(self, curso):
        subject = f"{curso} - CONTATO CURSO "
        context = {
            "nome": self.cleaned_data["nome"],
            "email": self.cleaned_data["email"],
            "msg": self.cleaned_data["msg"],
        }
        template_name = "courses/contact_email.html"
        send_mail_template(
            subject, template_name, context, [settings.CONTACT_EMAIL]
        )


ModuleFormSet = inlineformset_factory(
    Course, Module, fields=["title", "description"], extra=2, can_delete=True
)
