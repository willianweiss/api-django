from django.contrib import admin

from labqoda.configurations.models import DefaultInstructor

from .models import Reply, Thread


class ThreadAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "course",
        "views",
        "answers",
        "created",
        "updated",
    ]
    search_fields = ["title"]
    readonly_fields = ["views", "answers"]
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("content__module__course",)

    def course(self, obj):
        return obj.content.module.course


def set_approved(modeladmin, request, queryset):
    for obj in queryset:
        obj.status = Reply.APPROVED
        obj.save()


def set_disapproved(modeladmin, request, queryset):
    for obj in queryset:
        obj.status = Reply.DISAPPROVED
        obj.save()


def set_pending(modeladmin, request, queryset):
    for obj in queryset:
        obj.status = Reply.PENDING
        obj.save()


class ReplyInstanceInline(admin.StackedInline):
    model = Reply
    extra = 0
    fields = ("thread", "author", "status", "reply")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        default_instructor = DefaultInstructor.objects.last()
        """ Set instructor to default author """
        if default_instructor:
            if db_field.name == "author":
                kwargs["initial"] = default_instructor.instructor.id
        if db_field.name == "thread":
            try:
                reply_id = int(request.get_full_path().rsplit("/", 3)[1])
                thread_id = Reply.objects.get(pk=reply_id).thread.pk
                kwargs["queryset"] = Thread.objects.filter(pk=thread_id)
                kwargs["initial"] = Thread.objects.filter(pk=thread_id)
            except:  # noqa = E722
                pass
        return super(ReplyInstanceInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


class ReplyAdmin(admin.ModelAdmin):
    list_display = [
        "thread",
        "author",
        "status",
        "reply",
        "created",
    ]
    search_fields = ["thread__title", "author__email", "reply"]
    list_filter = ("status", "thread", "thread__content__module__course")
    actions = [set_approved, set_disapproved, set_pending]
    exclude = ["comment"]
    inlines = [ReplyInstanceInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(comment=None)


set_approved.short_description = "Atualizar para Aprovado!"
set_disapproved.short_description = "Atualizar para Reprovado!"
set_pending.short_description = "Atualizar para em Moderação!"


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Reply, ReplyAdmin)
