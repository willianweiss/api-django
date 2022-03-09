from django.db import models
from tinymce.models import HTMLField


class Question(models.Model):

    SINGLE_CHOICE = "single_choices"
    MULTIPLE_CHOICES = "multi_choices"

    TYPE_CHOICES = (
        (SINGLE_CHOICE, "Single Choice"),
        (MULTIPLE_CHOICES, "Multiple Choices"),
    )

    text = models.TextField()
    type = models.CharField(
        max_length=20, default=SINGLE_CHOICE, choices=TYPE_CHOICES
    )
    justification = HTMLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Quizz(models.Model):

    title = models.CharField(max_length=200)
    content = models.OneToOneField("courses.Content", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=1)
    questions = models.ManyToManyField(Question)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
