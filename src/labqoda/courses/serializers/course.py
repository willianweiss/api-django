from rest_framework import serializers

from labqoda.courses.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ["created_at", "updated_at", "image"]


class CourseEnrollmentSerializer(serializers.Serializer):
    code = serializers.CharField()
