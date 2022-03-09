import datetime

from django.contrib import admin

from .models import (
    CourseEnrollment,
    CourseProgress,
    CourseWatchedContent,
    Enrollment,
    PathEnrollment,
    PathProgress,
)


class PathEnrollmentInlineAdmin(admin.StackedInline):
    model = PathEnrollment
    extra = 0
    max_num = 1


class CourseEnrollmentInlineAdmin(admin.StackedInline):
    model = CourseEnrollment
    extra = 0
    max_num = 1


def set_approveds(modeladmin, request, queryset):
    for obj in queryset:
        obj.status = Enrollment.APROVADO
        obj.save()


set_approveds.short_description = "Colocar como aprovados!"


def set_pendente(modeladmin, request, queryset):
    for obj in queryset:
        obj.status = Enrollment.PENDENTE
        obj.save()


set_pendente.short_description = "Colocar como Pendentes!"


class EnrollmentAdmin(admin.ModelAdmin):
    model = Enrollment
    list_filter = ("status",)
    list_display = ["user", "status"]
    readonly_fields = [
        "code",
    ]
    inlines = (CourseEnrollmentInlineAdmin, PathEnrollmentInlineAdmin)
    actions = [set_approveds, set_pendente]
    search_fields = [
        "user__email",
    ]


def set_courseprogress_approved(modeladmin, request, queryset):
    for obj in queryset:
        obj.status = CourseProgress.FINISHED
        obj.date_of_issue = datetime.datetime.now()
        obj.save()


def set_courseprogress_started(modeladmin, request, queryset):
    for obj in queryset:
        obj.status = CourseProgress.STARTED
        obj.save()


set_courseprogress_approved.short_description = "Colocar como Aprovados!"
set_courseprogress_started.short_description = "Colocar como Iniciados!"


class CourseProgressAdmin(admin.ModelAdmin):
    model = CourseProgress
    list_display = [
        "user",
        "course",
        "status",
        "code",
    ]
    readonly_fields = [
        "code",
    ]
    search_fields = ["user__email", "course__name"]
    list_filter = ("status", "course")
    actions = [set_courseprogress_approved, set_courseprogress_started]


class PathProgressAdmin(admin.ModelAdmin):
    model = PathProgress
    list_display = ["user", "path", "status", "code"]
    readonly_fields = [
        "code",
    ]


class CourseWatchedContentAdmin(admin.ModelAdmin):
    model = CourseWatchedContent


admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(CourseProgress, CourseProgressAdmin)
admin.site.register(PathProgress, PathProgressAdmin)
admin.site.register(CourseWatchedContent, CourseWatchedContentAdmin)
