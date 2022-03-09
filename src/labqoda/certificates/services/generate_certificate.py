from django.template import Context, Template
from django.template.loader import get_template
from wkhtmltopdf.utils import render_pdf_from_template

from .utils import slugify_file


class GenerateCertificateService:

    certificat_path = "certificate.html"

    @classmethod
    def bind_text_certificate(cls, base_text, params):
        template = Template(base_text)
        context = Context(params)
        return template.render(context)

    @classmethod
    def make_certificate_pdf(cls, certificate_context, certificate_html):
        """
        Gera o certificado em PDF apartir do enrollment

        :param enrollment:
        :return: bytes with PDF content
        """

        return render_pdf_from_template(
            input_template=get_template(certificate_html),
            header_template=None,
            footer_template=None,
            context=certificate_context,
            request=None,
            cmd_options=None,
        )

    @classmethod
    def generate_filename(cls, contents):
        """
        :param array of string to join
        :return filename with _
        """
        slugify_name = slugify_file("_".join(contents))
        return slugify_name
