import django.contrib.auth.password_validation as validators
from django.core import exceptions
from rest_framework import serializers

from labqoda.enrollments.serializers import (
    CourseEnrollmentSerializers,
    CourseProgressSerializers,
    PathEnrollmentSerializers,
)

from .models import User


class UserDashboardSerializer(serializers.Serializer):
    courses_enrollments = serializers.ListSerializer(
        child=CourseEnrollmentSerializers()
    )
    paths_enrollments = serializers.ListSerializer(
        child=PathEnrollmentSerializers()
    )
    courses_in_progress = serializers.ListSerializer(
        child=CourseProgressSerializers()
    )
    total_courses = serializers.IntegerField()


class UserCreateSerializer(serializers.ModelSerializer):
    def validate(self, data):
        password = data.get("password")
        errors = dict()
        try:
            validators.validate_password(password=password, user=User)

        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserCreateSerializer, self).validate(data)

    class Meta:
        model = User
        fields = ["email", "password"]


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "fullname",
            "email",
            "is_staff",
            "is_active",
            "is_active",
            "is_trusty",
        ]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
