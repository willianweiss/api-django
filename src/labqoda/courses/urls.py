from django.urls import path

from .views import (
    ContentCreateListView,
    ContentDetailView,
    ContentItemsView,
    CoursesDetailView,
    CoursesEnrollmentView,
    CoursesListCreateView,
    CoursesUpdateDeleteView,
    ModuleCreateListView,
    ModuleDetailView,
    PathCourseDetailView,
    PathCourseListView,
    PathDetailView,
    PathListView,
    VideoContentListView,
)

urlpatterns = [
    path("", CoursesListCreateView.as_view(), name="courses-list"),
    path(
        "<int:pk>/",
        CoursesUpdateDeleteView.as_view(),
        name="courses-update-delete",
    ),
    path("path/", PathListView.as_view(), name="path-list",),
    path("path/<slug:slug>/", PathDetailView.as_view(), name="path-detail",),
    path(
        "path/<slug:slug>/course/",
        PathCourseListView.as_view(),
        name="path-course-list",
    ),
    path(
        "path/<slug:slug>/course/<int:pk>/",
        PathCourseDetailView.as_view(),
        name="path-course-detail",
    ),
    path("<slug:slug>/", CoursesDetailView.as_view(), name="courses-detail"),
    path(
        "<slug:slug>/enrollment/",
        CoursesEnrollmentView.as_view(),
        name="courses-enrollment",
    ),
    path(
        "<slug:slug>/module/",
        ModuleCreateListView.as_view(),
        name="module-list",
    ),
    path(
        "<slug:slug>/module/<int:pk>/",
        ModuleDetailView.as_view(),
        name="module-detail",
    ),
    path(
        "module/<int:pk>/content/",
        ContentCreateListView.as_view(),
        name="content-list",
    ),
    path(
        "module/<int:module_id>/content/<int:pk>/",
        ContentDetailView.as_view(),
        name="content-detail",
    ),
    path(
        "module/<int:module_id>/content/<int:pk>/items/",
        ContentItemsView.as_view(),
        name="content-items",
    ),
    path(
        "video/<int:pk>/", VideoContentListView.as_view(), name="video-detail",
    ),
]
