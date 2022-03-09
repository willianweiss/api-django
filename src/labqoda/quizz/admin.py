import nested_admin
from django.contrib import admin

from labqoda.quizz.forms import QuestionForm

from .models import Choice, Question, Quizz


class ChoiceInlineAdmin(nested_admin.NestedStackedInline):
    extra = 0
    max_num = 10
    model = Choice


@admin.register(Question)
class QuestionAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        ChoiceInlineAdmin,
    ]
    form = QuestionForm
    list_display = ("text", "type")


@admin.register(Quizz)
class QuizzAdmin(nested_admin.NestedModelAdmin):

    filter_horizontal = ("questions",)
