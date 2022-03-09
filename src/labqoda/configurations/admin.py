from django.contrib import admin

from .models import Contact, DefaultInstructor


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):

    list_display = [
        "name",
        "email",
        "message",
    ]


admin.site.register(DefaultInstructor)
