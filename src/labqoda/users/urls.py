from django.urls import include, path

from .views import (
    ChangePasswordView,
    UserDashboard,
    UserDetail,
    UserRegisterView,
)

urlpatterns = [
    path("me/", UserDetail.as_view(), name="user-detail",),
    path("me/dashboard/", UserDashboard.as_view(), name="user-dashboard"),
    path(
        "me/password-change/",
        ChangePasswordView.as_view(),
        name="password-change",
    ),
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path(
        "password-reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
]
