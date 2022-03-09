from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from labqoda import __version__


class IndexSerializer(serializers.Serializer):
    version = serializers.CharField()


class IndexView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = IndexSerializer

    def get(self, request, format=None):
        serializer = IndexSerializer(data={"version": __version__})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)
