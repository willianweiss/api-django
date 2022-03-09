import uuid

from django.db import models
from tinymce.models import HTMLField

from labqoda.courses.models import Course, Path


def normalize_template_tags_name(text):
    text = text.replace("{{ Name }}", "{{ name }}")
    text = text.replace("{{ Email }}", "{{ email }}")
    text = text.replace("{{ Course_duration }}", "{{ course_duration }}")
    text = text.replace("{{ Date_of_issue }}", "{{ date_of_issue }}")
    text = text.replace("{{ Verification_code }}", "{{ verification_code }}")
    return text


class CertificateBaseTemplate(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=100)
    image = models.ImageField()
    text = HTMLField()
    version = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.text = normalize_template_tags_name(self.text)
        return super(CertificateBaseTemplate, self).save(*args, **kwargs)


class CourseCertificate(CertificateBaseTemplate):
    class Meta:
        verbose_name = "Certificado de Curso"
        verbose_name_plural = "Certificados de Cursos"

    public = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class PathCertificate(CertificateBaseTemplate):
    class Meta:
        verbose_name = "Certificado de Trilha"
        verbose_name_plural = "Certificados de Trilhas"

    public = models.BooleanField(default=False)
    path = models.ForeignKey(Path, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class UserCertificate(models.Model):

    certificate_code = models.UUIDField(default=uuid.uuid4)
    text = HTMLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.certificate_code)

    def save(self, *args, **kwargs):
        self.text = normalize_template_tags_name(self.text)
        return super(UserCertificate, self).save(*args, **kwargs)
