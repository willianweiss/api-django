from django.core.files.storage import FileSystemStorage
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.template.loader import render_to_string
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from weasyprint import HTML

from labqoda.enrollments.models import CourseProgress, PathProgress

from .models import CourseCertificate, PathCertificate, UserCertificate
from .services.generate_certificate import GenerateCertificateService
from .services.validate_certificate import ValidateCertificateService


class CourseCertificateView(APIView):
    def get_course_context(self, course_progress):
        if course_progress.course_enrollment:
            user = course_progress.course_enrollment.enrollment.user
        else:
            user = course_progress.path_enrollment.enrollment.user

        course = course_progress.course
        course_certificate = (
            course_progress.course.coursecertificate_set.last()
        )

        context = {
            "name": user.fullname
            if user.fullname
            else f"{user.first_name} {user.last_name}",
            "email": user.email,
            "course_name": course.name,
            "course_duration": course.duration,
            "date_of_issue": course_progress.date_of_issue,
            "verification_code": course_progress.code,
        }

        print(context)
        return course_certificate, context

    def get_manual_certificate(self, course_progress):
        user_certificate = UserCertificate.objects.filter(
            certificate_code=course_progress.code, is_active=True
        ).last()
        return user_certificate

    @extend_schema(description="Get Course Certificate",)
    def get(self, request, *args, **kwargs):
        try:
            enrollment_code = self.kwargs["enrollment_code"]
            course_progress = ValidateCertificateService.validate_course_code(
                enrollment_code, request.user
            )

            custom_certificate_text = None
            user_certificate = self.get_manual_certificate(course_progress)
            if user_certificate:
                custom_certificate_text = user_certificate.text

            certificate_class, context = self.get_course_context(
                course_progress
            )

            if custom_certificate_text:
                certificate_text_to_use = custom_certificate_text
            else:
                certificate_text_to_use = certificate_class.text

            certificate_text = GenerateCertificateService.bind_text_certificate(  # noqa
                certificate_text_to_use, context
            )

            if not certificate_class.public:
                raise ValueError("Criando Certificado")

            context.update(
                {
                    "certificate": model_to_dict(certificate_class),
                    "certificate_text": certificate_text,
                    "course_progress": course_progress,
                }
            )

            filename = f"certificate_{context.get('verification_code')}.pdf"

            html_string = render_to_string("certificate.html", context)
            html = HTML(string=html_string)
            html.write_pdf(target=f"/tmp/{filename}")

            fs = FileSystemStorage("/tmp")
            with fs.open(filename) as pdf:
                response = HttpResponse(pdf, content_type="application/pdf")
                response[
                    "Content-Disposition"
                ] = f'attachment; filename="{filename}"'  # noqa
                return response

        except Exception:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class PathCertificateView(APIView):
    def get_path_context(self, path_progress):
        user = path_progress.enrollment.enrollment.user
        path = path_progress.path

        path_certificate = path_progress.path.pathcertificate_set.last()

        context = {
            "name": user.fullname
            if user.fullname
            else f"{user.first_name} {user.last_name}",
            "email": user.email,
            "path_name": path.name,
            "mini_description": path.minidesc,
            "verification_code": path_progress.code,
        }
        return path_certificate, context

    @extend_schema(description="Get Path Certificate",)
    def get(self, request, *args, **kwargs):
        try:
            enrollment_code = self.kwargs["enrollment_code"]
            path_progress = ValidateCertificateService.validate_path_code(
                enrollment_code, request.user
            )

            certificate_class, context = self.get_path_context(path_progress)

            certificate_text = GenerateCertificateService.bind_text_certificate(  # noqa
                certificate_class.text, context
            )

            if not certificate_class.public:
                raise ValueError("Criando Certificado")

            context.update(
                {
                    "certificate": model_to_dict(certificate_class),
                    "certificate_text": certificate_text,
                }
            )

            filename = f"certificate_{context.get('verification_code')}.pdf"

            html_string = render_to_string("certificate.html", context)
            html = HTML(string=html_string)
            html.write_pdf(target=f"/tmp/{filename}")

            fs = FileSystemStorage("/tmp")
            with fs.open(filename) as pdf:
                response = HttpResponse(pdf, content_type="application/pdf")
                response[
                    "Content-Disposition"
                ] = f'attachment; filename="{filename}"'  # noqa
                return response

        except Exception:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ListUserCertificates(APIView):
    @extend_schema(description="Get User Certificates",)
    def get(self, request, *args, **kwargs):
        paths = PathProgress.objects.filter(
            status=PathProgress.FINISHED, user=self.request.user
        )

        courses = CourseProgress.objects.filter(
            status=CourseProgress.FINISHED, user=self.request.user
        )

        data = {
            "courses_certificates": courses,
            "paths_certificates": paths,
        }

        return Response(data, status=status.HTTP_200_OK)


class BaseCertificateExample:
    def get_context(self, class_certificate):
        context = {
            "name": "Teste Silva",
            "email": "teste@gmail.com",
            "path_name": "Curso/Trilha de X",
            "mini_description": "mini desc do curso/trilha",
            "date_of_issue": "10 de maio de 2020",
            "verification_code": "04869e9c-c4e5-4ca6-a5b1-70490ecd4901",
        }

        certificate_text = GenerateCertificateService.bind_text_certificate(
            class_certificate.text, context
        )

        context = {
            "certificate": class_certificate,
            "certificate_text": certificate_text,
        }

        return context


class CourseCertificateExampleView(APIView, BaseCertificateExample):
    def get(self, request, *args, **kwargs):
        course_certificate_id = self.kwargs["course_certificate_id"]
        course_certificate = CourseCertificate.objects.get(
            id=course_certificate_id
        )
        html_string = render_to_string(
            "test_certificate.html", self.get_context(course_certificate)
        )
        html = HTML(string=html_string)
        html.write_pdf(target="/tmp/test_certificate.pdf")

        fs = FileSystemStorage("/tmp")
        with fs.open("test_certificate.pdf") as pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            response[
                "Content-Disposition"
            ] = 'attachment; filename="test_certificate.pdf"'  # noqa
            return response


class RenderPathCertificateExampleView(APIView, BaseCertificateExample):
    def get(self, request, *args, **kwargs):
        path_certificate_id = self.kwargs["path_certificate_id"]
        path_certificate = PathCertificate.objects.get(id=path_certificate_id)

        html_string = render_to_string(
            "test_certificate.html", self.get_context(path_certificate)
        )
        html = HTML(string=html_string)
        html.write_pdf(target="/tmp/test_certificate.pdf")

        fs = FileSystemStorage("/tmp")
        with fs.open("test_certificate.pdf") as pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            response[
                "Content-Disposition"
            ] = 'attachment; filename="test_certificate.pdf"'  # noqa
            return response
