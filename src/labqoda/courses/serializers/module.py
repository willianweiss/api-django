from rest_framework import serializers

from labqoda.courses.models import Course, Module


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"
        depth = 1


class ModuleCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    course = serializers.CharField()

    class Meta:
        model = Module
        exclude = ["order"]

    def create(self, data):
        course = Course.objects.get(slug=data["course"])
        module = Module(
            course=course,
            title=data.get("title"),
            description=data.get("description"),
            tags=data.get("tags"),
        )
        module.save()
        return module
