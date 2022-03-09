from django.urls import path

from .views import ContactDetail, ContactList

urlpatterns = [
    path("contacts/", ContactList.as_view(), name="contact-list"),
    path(
        "contacts/<int:pk>/", ContactDetail.as_view(), name="contact-detail",
    ),
]
