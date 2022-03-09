from rest_framework import serializers

from labqoda.courses.models import Content, File, Image, Module, Text, Video
from labqoda.quizz.serializers import QuizzSerializer
from labqoda.users.models import User


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):

    image = serializers.CharField()

    class Meta:
        model = Image
        fields = "__all__"


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = "__all__"


class FileSerializer(serializers.ModelSerializer):

    filename = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = "__all__"

    def get_filename(self, obj):
        try:
            return obj.get_filename()
        except Exception:
            return "Arquivo"


class ContentItemsSerializer(serializers.ModelSerializer):

    videos = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    texts = serializers.SerializerMethodField()
    files = serializers.SerializerMethodField()
    quizz = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = "__all__"

    def get_videos(self, obj):
        serializer = VideoSerializer(obj.video_set.all(), many=True)
        return serializer.data

    def get_images(self, obj):
        serializer = ImageSerializer(obj.image_set.all(), many=True)
        return serializer.data

    def get_texts(self, obj):
        serializer = TextSerializer(obj.text_set.all(), many=True)
        return serializer.data

    def get_files(self, obj):
        serializer = FileSerializer(obj.file_set.all(), many=True)
        return serializer.data

    def get_quizz(self, obj):
        if hasattr(obj, "quizz"):
            serializer = QuizzSerializer(obj.quizz, many=False)
            return serializer.data
        return None


class ContentBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"


class ContentCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    module = serializers.CharField()
    instructor = serializers.CharField()

    class Meta:
        model = Content
        exclude = ["order"]

    def create(self, data):
        module = Module.objects.get(pk=data["module"])
        instructor = User.objects.get(pk=data["instructor"])
        content = Content(
            module=module,
            duration=data.get("duration"),
            title=data.get("title"),
            instructor=instructor,
        )
        content.save()
        return content
