from django.contrib import admin
from django.utils.html import format_html

from .models import CourseCertificate, PathCertificate


@admin.register(CourseCertificate)
class CourseCertificateAdmin(admin.ModelAdmin):

    list_display = [
        "title",
        "course",
        "image",
        "version",
        "certificate_example",
    ]
    add_form_template = (
        "admin/certificates/coursecertificate/add_coursecertificate.html"
    )
    change_form_template = (
        "admin/certificates/coursecertificate/add_coursecertificate.html"
    )

    def certificate_example(self, obj):
        return format_html(
            '<a href="https://lab.qoda.com.br/certificates/'
            'certificate-course-example/{0}"> Clique aqui! </a>',
            obj.id,
        )

    certificate_example.allow_tags = True
    certificate_example.short_description = "Exemplo de Certificado"


@admin.register(PathCertificate)
class PathCertificateAdmin(admin.ModelAdmin):

    list_display = ["title", "path", "image", "version", "certificate_example"]
    add_form_template = (
        "admin/certificates/pathcertificate/add_pathcertificate.html"
    )
    change_form_template = (
        "admin/certificates/pathcertificate/add_pathcertificate.html"
    )

    def certificate_example(self, obj):
        return format_html(
            '<a href="https://lab.qoda.com.br/certificates/'
            'certificate-path-example/{0}"> Clique aqui! </a>',
            obj.id,
        )

    certificate_example.allow_tags = True
    certificate_example.short_description = "Exemplo de Certificado"
