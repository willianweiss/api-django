from django.urls import path

from .views import QuizzDetail, QuizzList

urlpatterns = [
    path("", QuizzList.as_view(), name="quizz-list"),
    path("<int:pk>/", QuizzDetail.as_view(), name="quizz-detail",),
]
