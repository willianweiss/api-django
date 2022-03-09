from django.urls import path

from .views import (
    CourseCertificateExampleView,
    CourseCertificateView,
    ListUserCertificates,
    PathCertificateView,
    RenderPathCertificateExampleView,
)

urlpatterns = [
    path(
        "course/<slug:enrollment_code>/",
        CourseCertificateView.as_view(),
        name="certificate-course",
    ),
    path(
        "path/<slug:enrollment_code>/",
        PathCertificateView.as_view(),
        name="certificate-path",
    ),
    path("user/", ListUserCertificates.as_view(), name="certificate-user"),
    path(
        "certificate-course-example/<int:course_certificate_id>/",
        CourseCertificateExampleView.as_view(),
        name="certificate-course-example",
    ),
    path(
        "certificate-path-example/<int:path_certificate_id>/",
        RenderPathCertificateExampleView.as_view(),
        name="certificate-path-example",
    ),
]
