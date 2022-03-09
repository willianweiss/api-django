from rest_framework import serializers

from .models import Choice, Question, Quizz


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(source="choice_set", many=True)

    class Meta:
        model = Question
        fields = "__all__"


class QuizzSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quizz
        fields = "__all__"
