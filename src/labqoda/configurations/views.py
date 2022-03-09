from rest_framework.generics import ListCreateAPIView, RetrieveAPIView

from .models import Contact
from .serializers import ContactSerializer


class ContactList(ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ContactDetail(RetrieveAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
