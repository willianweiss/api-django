"""Labqoda API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from labqoda.index.views import IndexView

urlpatterns = [
    path("", IndexView.as_view()),
    path("admin/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url="/schema/"),
        name="swagger-ui",
    ),
    path("auth/", include("rest_framework_social_oauth2.urls"), name="auth"),
    path("catalog/", include("labqoda.catalog.urls"), name="catalog"),
    path(
        "configurations/",
        include("labqoda.configurations.urls"),
        name="configurations",
    ),
    path("users/", include("labqoda.users.urls"), name="users"),
    path("quizz/", include("labqoda.quizz.urls"), name="quizz"),
    path("forum/", include("labqoda.forum.urls"), name="forum"),
    path("courses/", include("labqoda.courses.urls"), name="courses"),
    path(
        "certificates/",
        include("labqoda.certificates.urls"),
        name="certificates",
    ),
]
