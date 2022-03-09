from rest_framework import serializers

from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Contact
        fields = ["id", "name", "email", "message"]
