from rest_framework import serializers

from labqoda.courses.models import Path, PathCourse


class PathSerializer(serializers.ModelSerializer):
    class Meta:
        model = Path
        fields = "__all__"
        depth = 1


class PathCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PathCourse
        fields = "__all__"
        depth = 1
