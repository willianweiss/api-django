from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from labqoda.enrollments.models import (
    CourseEnrollment,
    CourseProgress,
    PathEnrollment,
)
from labqoda.enrollments.serializers import (
    CourseEnrollmentSerializers,
    CourseProgressSerializers,
    PathEnrollmentSerializers,
)

from .models import User
from .serializers import (
    ChangePasswordSerializer,
    UserCreateSerializer,
    UserDashboardSerializer,
    UserSerializer,
)


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserCreateSerializer,
        responses={status.HTTP_201_CREATED: UserSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj


class UserDashboard(APIView):
    @extend_schema(responses={status.HTTP_200_OK: UserDashboardSerializer},)
    def get(self, request, format=None):
        user = self.request.user

        subtotal_path_enrollments = (
            PathEnrollment.objects.filter(enrollment__user=user)
            .values("path__courses")
            .count()
        )
        subtotal_courses_enrollments = CourseEnrollment.objects.filter(
            enrollment__user=user
        ).count()

        total_courses = (
            subtotal_courses_enrollments + subtotal_path_enrollments
        )

        courses_enrollments = CourseEnrollment.objects.filter(
            enrollment__user=user
        )
        courses_enrollments_serializer = CourseEnrollmentSerializers(
            courses_enrollments, many=True
        )

        path_enrollments = PathEnrollment.objects.filter(enrollment__user=user)
        path_enrollments_serializer = PathEnrollmentSerializers(
            path_enrollments, many=True
        )

        courses_in_progress = CourseProgress.objects.filter(
            user=user, status=CourseProgress.STARTED
        )
        courses_in_progress_serializer = CourseProgressSerializers(
            courses_in_progress, many=True
        )

        data = {
            "courses_enrollments": courses_enrollments_serializer.data,
            "paths_enrollments": path_enrollments_serializer.data,
            "courses_in_progress": courses_in_progress_serializer.data,
            "total_courses": total_courses,
        }

        serializer = UserDashboardSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not self.object.check_password(serializer.data.get("old_password")):
            return Response(
                {"old_password": ["Wrong password."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.object.set_password(serializer.data.get("new_password"))
        self.object.save()
        response = {
            "status": "success",
            "code": status.HTTP_200_OK,
            "message": "Password updated successfully",
            "data": [],
        }

        return Response(response)
