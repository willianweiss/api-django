import django_filters

from .models import Course, Path


class CoursesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name")
    tags = django_filters.CharFilter(
        field_name="tags", lookup_expr="tags__name"
    )

    class Meta:
        model = Course
        fields = [
            "name",
            "tags",
        ]


class PathFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name")
    tags = django_filters.CharFilter(
        field_name="tags", lookup_expr="tags__name"
    )

    class Meta:
        model = Path
        fields = [
            "name",
            "tags",
        ]
