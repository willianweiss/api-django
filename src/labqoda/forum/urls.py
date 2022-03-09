from django.urls import path

from .views import (
    ReplyDetailView,
    ReplyListView,
    ThreadDetailView,
    ThreadListView,
)

urlpatterns = [
    path("thread/", ThreadListView.as_view(), name="thread-list"),
    path(
        "thread/<slug:slug>/", ThreadDetailView.as_view(), name="thread-detail"
    ),
    path("reply/", ReplyListView.as_view(), name="reply-list"),
    path("reply/<int:pk>/", ReplyDetailView.as_view(), name="reply-detail"),
]
