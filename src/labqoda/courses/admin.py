import nested_admin
from django.contrib import admin

from labqoda.configurations.models import DefaultInstructor
from labqoda.quizz.models import Quizz

from .forms import VideoUploadForm
from .models import (
    Content,
    Course,
    File,
    Image,
    Module,
    Path,
    PathCourse,
    Subject,
    Text,
    Video,
)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):

    list_display = ["title", "slug"]
    prepopulated_fields = {"slug": ("title",)}


class ModuleInline(admin.StackedInline):
    model = Module
    extra = 0
    max_num = 100


class ImageInlineAdmin(nested_admin.NestedStackedInline):
    model = Image
    extra = 0
    max_num = 5
    sortable_field_name = "order"


class VideoInlineAdmin(nested_admin.NestedStackedInline):
    model = Video
    extra = 0
    max_num = 1
    sortable_field_name = "order"
    form = VideoUploadForm


class TextInlineAdmin(nested_admin.NestedStackedInline):
    model = Text
    extra = 0
    max_num = 1
    sortable_field_name = "order"


class FileInlineAdmin(nested_admin.NestedStackedInline):
    model = File
    extra = 0
    max_num = 10
    sortable_field_name = "order"


class QuizzInlineAdmin(nested_admin.NestedStackedInline):
    model = Quizz
    sortable_field_name = "order"
    extra = 0
    filter_horizontal = ("questions",)


class ContentAdmin(nested_admin.NestedModelAdmin):
    model = Content
    list_display = ["title", "course", "module", "order"]
    search_fields = ["module", "module__course", "title"]
    exclude = ["duration"]
    inlines = (
        ImageInlineAdmin,
        VideoInlineAdmin,
        TextInlineAdmin,
        FileInlineAdmin,
        QuizzInlineAdmin,
    )
    list_filter = ("module__course",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Set instructor to default instructor registred """
        default_instructor = DefaultInstructor.objects.last()
        if default_instructor:
            if db_field.name == "instructor":
                kwargs["initial"] = default_instructor.instructor.id
        return super(ContentAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def course(self, obj):
        return obj.module.course


class ContentInline(nested_admin.NestedStackedInline):
    model = Content
    extra = 0
    max_num = 100
    inlines = (
        ImageInlineAdmin,
        VideoInlineAdmin,
        TextInlineAdmin,
        FileInlineAdmin,
        QuizzInlineAdmin,
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Set instructor to default instructor registred """
        default_instructor = DefaultInstructor.objects.last()
        if default_instructor:
            if db_field.name == "instructor":
                kwargs["initial"] = default_instructor.instructor.id
        return super(ContentInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


class ModuleAdmin(nested_admin.NestedModelAdmin):
    list_display = ["title", "course", "description", "tags", "order"]
    search_fields = ["course__name", "title"]
    inlines = [ContentInline]


class CourseAdmin(admin.ModelAdmin):
    list_display = ["name", "subject", "slug", "start_date", "created_at"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ModuleInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Set instructor to default instructor registred """
        default_instructor = DefaultInstructor.objects.last()
        if default_instructor:
            if db_field.name == "instructor":
                kwargs["initial"] = default_instructor.instructor.id
        return super(CourseAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


class PathCourseInlineAdmin(admin.StackedInline):
    model = PathCourse
    extra = 1
    max_num = 100


class PathAdmin(admin.ModelAdmin):
    list_display = ["name", "tags", "slug", "description", "minidesc", "image"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [PathCourseInlineAdmin]


admin.site.register(Course, CourseAdmin)
admin.site.register(Path, PathAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Content, ContentAdmin)
