from rest_framework import serializers

from .models import (
    CourseEnrollment,
    CourseProgress,
    CourseWatchedContent,
    Enrollment,
    PathEnrollment,
    PathProgress,
)


class EnrollmentCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = "__all__"
        depth = 1


class EnrollmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = "__all__"
        depth = 1


class CourseEnrollmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = CourseEnrollment
        fields = "__all__"
        depth = 1


class PathEnrollmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = PathEnrollment
        fields = "__all__"
        depth = 1


class CourseProgressSerializers(serializers.ModelSerializer):
    class Meta:
        model = CourseProgress
        fields = "__all__"
        depth = 1


class CourseWatchedContentSerializers(serializers.ModelSerializer):
    class Meta:
        model = CourseWatchedContent
        fields = "__all__"
        depth = 1


class PathProgressSerializers(serializers.ModelSerializer):
    class Meta:
        model = PathProgress
        fields = "__all__"
        depth = 1
