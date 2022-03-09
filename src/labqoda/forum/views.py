from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .filters import ReplayFilter
from .models import Reply, Thread
from .serializers import (
    ReplyCreateSerializer,
    ReplySerializer,
    ReplyUpdateSerializer,
    ThreadCreateSerializer,
    ThreadSerializer,
)


class ThreadListView(ListCreateAPIView):
    queryset = Thread.objects.all()

    @extend_schema(responses={status.HTTP_200_OK: ThreadSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        self.serializer_class = ThreadSerializer
        return self.list(request, *args, **kwargs)

    @extend_schema(
        request=ThreadCreateSerializer,
        responses={status.HTTP_201_CREATED: ThreadSerializer},
    )
    def post(self, request, *args, **kwargs):
        self.serializer_class = ThreadCreateSerializer
        return self.create(request, *args, **kwargs)


class ThreadDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    lookup_field = "slug"


class ReplyListView(ListCreateAPIView):
    queryset = Reply.objects.all()
    filterset_class = ReplayFilter

    @extend_schema(responses={status.HTTP_200_OK: ReplySerializer(many=True)})
    def get(self, request, *args, **kwargs):
        self.serializer_class = ReplySerializer
        return self.list(request, *args, **kwargs)

    @extend_schema(
        request=ReplyCreateSerializer,
        responses={status.HTTP_201_CREATED: ReplySerializer},
    )
    def post(self, request, *args, **kwargs):
        self.serializer_class = ReplyCreateSerializer
        return self.create(request, *args, **kwargs)


class ReplyDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    @extend_schema(
        request=ReplyUpdateSerializer,
        responses={status.HTTP_200_OK: ReplySerializer},
    )
    def put(self, request, *args, **kwargs):
        self.serializer_class = ReplyUpdateSerializer
        return self.update(request, *args, **kwargs)

    @extend_schema(
        request=ReplyUpdateSerializer,
        responses={status.HTTP_200_OK: ReplySerializer},
    )
    def patch(self, request, *args, **kwargs):
        self.serializer_class = ReplyUpdateSerializer
        return self.partial_update(request, *args, **kwargs)
