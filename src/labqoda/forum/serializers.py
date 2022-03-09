from rest_framework import serializers

from labqoda.courses.models import Content
from labqoda.helpers.drf.fields import CustomChoicesField
from labqoda.users.models import User

from .choices import STATUS_BY_SERIALIZER
from .models import Reply, Thread


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    author_email = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = "__all__"

    def get_author(self, obj):
        if obj.author.fullname:
            return obj.author.fullname
        return "{} {}".format(obj.author.first_name, obj.author.last_name)

    def get_author_email(self, obj):
        return obj.author.email

    def get_comments(self, obj):
        comments = Reply.objects.filter(
            comment=obj.id, status__in=[Reply.APPROVED, Reply.PENDING]
        )
        serialized_comments = ReplySerializer(comments, many=True)
        return serialized_comments.data


class ReplyCreateSerializer(serializers.ModelSerializer):
    thread_id = serializers.IntegerField()
    comment_id = serializers.IntegerField(required=False)
    status = CustomChoicesField(choices=STATUS_BY_SERIALIZER, required=False)
    author_id = serializers.CharField()

    class Meta:
        model = Reply
        fields = [
            "thread_id",
            "comment_id",
            "reply",
            "correct",
            "status",
            "author_id",
        ]

    def create(self, data):
        thread = Thread.objects.get(pk=data["thread_id"])
        author = User.objects.get(pk=data["author_id"])

        if data.get("comment_id"):
            comment = Reply.objects.get(pk=data["comment_id"])
            data["comment_id"] = comment

        reply = Reply(
            reply=data["reply"],
            comment=data.get("comment_id"),
            correct=data.get("correct"),
            status=data.get("status"),
            author=author,
            thread=thread,
        )
        reply.save()
        return reply


class ReplyUpdateSerializer(serializers.ModelSerializer):
    status = CustomChoicesField(choices=STATUS_BY_SERIALIZER, required=False)

    class Meta:
        model = Reply
        fields = ["reply", "correct", "status"]


class ThreadSerializer(serializers.ModelSerializer):
    replys = serializers.SerializerMethodField()
    views = serializers.IntegerField(required=False)
    answers = serializers.IntegerField(required=False)

    class Meta:
        model = Thread
        fields = ["title", "slug", "content", "views", "answers", "replys"]
        read_only_fields = ["id", "replys", "content"]

    def get_replys(self, obj):
        replys = Reply.objects.filter(
            thread=obj.id, status__in=[Reply.APPROVED, Reply.PENDING]
        )
        serialized_replys = ReplySerializer(replys, many=True)
        return serialized_replys.data

    def create(self, data):
        content, __ = Content.objects.get_or_create(pk=data["content"])
        thread = Thread(
            title=data["title"], slug=data["slug"], content=content
        )
        thread.save()
        return thread


class ThreadCreateSerializer(serializers.ModelSerializer):
    content_id = serializers.IntegerField(required=True)
    views = serializers.IntegerField(required=False)
    answers = serializers.IntegerField(required=False)

    class Meta:
        model = Thread
        fields = ["title", "slug", "content_id", "views", "answers"]
        read_only_fields = ["id", "replys"]

    def create(self, data):
        content = Content.objects.get(pk=data["content_id"])
        thread = Thread(
            title=data["title"], slug=data["slug"], content=content
        )
        thread.save()
        return thread
