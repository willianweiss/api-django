import django_filters

from .choices import STATUS_BY_SERIALIZER
from .models import Reply


class ReplayFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=STATUS_BY_SERIALIZER)
    thread_id = django_filters.CharFilter(
        field_name="thread", lookup_expr="thread__pk"
    )
    thread_slug = django_filters.CharFilter(
        field_name="thread", lookup_expr="thread__slug"
    )
    comment_id = django_filters.NumberFilter(
        field_name="comment", lookup_expr="comment__pk"
    )

    class Meta:
        model = Reply
        fields = [
            "status",
            "thread_id",
            "thread_slug",
            "comment_id",
        ]
