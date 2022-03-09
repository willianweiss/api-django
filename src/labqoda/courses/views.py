from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from labqoda.enrollments.models import CourseEnrollment, Enrollment
from labqoda.users.models import User

from .filters import CoursesFilter, PathFilter
from .models import Content, Course, Module, Path, PathCourse
from .serializers import (
    ContentBaseSerializer,
    ContentCreateSerializer,
    ContentItemsSerializer,
    CourseCreateSerializer,
    CourseSerializer,
    ModuleCreateSerializer,
    ModuleSerializer,
    PathCourseSerializer,
    PathSerializer,
)
from .services.vdocipher import VdoCipher


class CoursesListCreateView(ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_class = CoursesFilter

    @extend_schema(
        request=CourseCreateSerializer,
        responses={status.HTTP_201_CREATED: CourseSerializer},
        description="Create Course",
    )
    def post(self, request, *args, **kwargs):
        self.permission_classes = [IsAdminUser]
        self.serializer_class = CourseCreateSerializer
        return self.create(request, *args, **kwargs)


class CoursesDetailView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = "slug"


class CoursesUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CoursesEnrollmentView(APIView):
    @transaction.atomic
    def _create_course_enrolment(self, user, course):
        enrollment = Enrollment.objects.create(user=user)
        course_enrollment = CourseEnrollment.objects.create(
            enrollment=enrollment, course=course
        )
        enrollment.save()
        course_enrollment.save()
        return enrollment.code

    @extend_schema(description="Create Course Enrollment",)
    def post(self, request, *args, **kwargs):
        user = request.user
        course = get_object_or_404(Course, slug=kwargs["slug"])

        course_enrollment = CourseEnrollment.objects.filter(
            enrollment__user=user, course=course
        ).first()

        if course_enrollment:
            return Response(
                {"code": course_enrollment.enrollment.code},
                status=status.HTTP_200_OK,
            )

        code = self._create_course_enrolment(user=user, course=course)

        return Response({"code": code}, status=status.HTTP_200_OK)


class PathListView(ListAPIView):
    queryset = Path.objects.all()
    serializer_class = PathSerializer
    filterset_class = PathFilter


class PathDetailView(RetrieveAPIView):
    queryset = Path.objects.all()
    serializer_class = PathSerializer
    lookup_field = "slug"


class PathCourseListView(ListAPIView):
    serializer_class = PathCourseSerializer

    def get_queryset(self):
        path = get_object_or_404(Path, slug=self.kwargs["slug"])
        return PathCourse.objects.filter(path=path)


class PathCourseDetailView(RetrieveAPIView):
    queryset = PathCourse.objects.all()
    serializer_class = PathCourseSerializer

    def get_object(self, queryset=None):
        path = get_object_or_404(Path, slug=self.kwargs["slug"])
        return get_object_or_404(PathCourse, path=path, pk=self.kwargs["pk"])


class ModuleCreateListView(ListCreateAPIView):
    serializer_class = ModuleSerializer

    def get_queryset(self):
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        return Module.objects.filter(course=course)

    @extend_schema(
        request=ModuleCreateSerializer,
        responses={status.HTTP_201_CREATED: ModuleSerializer},
        description="Module Create",
    )
    def post(self, request, *args, **kwargs):
        self.serializer_class = ModuleCreateSerializer
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        get_object_or_404(Course, slug=self.kwargs["slug"])
        data = request.data
        data["course"] = kwargs["slug"]
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ModuleDetailView(RetrieveAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def get_object(self, queryset=None):
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        return get_object_or_404(Module, course=course, pk=self.kwargs["pk"])


class ContentCreateListView(ListCreateAPIView):
    serializer_class = ContentBaseSerializer

    def get_queryset(self):
        module = get_object_or_404(Module, pk=self.kwargs["pk"])
        return Content.objects.filter(module=module)

    @extend_schema(
        request=ContentCreateSerializer,
        responses={status.HTTP_201_CREATED: ContentBaseSerializer},
        description="Content Create",
    )
    def post(self, request, *args, **kwargs):
        self.serializer_class = ContentCreateSerializer
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        get_object_or_404(Module, pk=self.kwargs["pk"])
        instructor = User.objects.filter(pk=request.data.get("instructor"))

        if not instructor:
            Response(
                "Instructor not found", status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data
        data["module"] = kwargs["pk"]

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ContentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentBaseSerializer

    def get_object(self, queryset=None):
        module = get_object_or_404(Module, pk=self.kwargs["module_id"])
        return get_object_or_404(Content, module=module, pk=self.kwargs["pk"])


class ContentItemsView(APIView):
    serializer_class = ContentItemsSerializer

    @extend_schema(description="Get Content Items",)
    def get(self, request, *args, **kwargs):
        module = get_object_or_404(Module, pk=self.kwargs["module_id"])
        content = get_object_or_404(
            Content, module=module, pk=self.kwargs["pk"]
        )

        serializer = ContentItemsSerializer(instance=content)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VideoContentListView(APIView):
    @extend_schema(description="Get Video Detail",)
    def get(self, request, *args, **kwargs):
        vdochiper = VdoCipher()
        context = vdochiper.get_video_render(self.kwargs["pk"])
        return Response(context, status=status.HTTP_200_OK)
