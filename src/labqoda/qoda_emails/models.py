from django.db import models

from labqoda.courses.models import Course


class EmailUsersCourse(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    text = models.TextField()
    send = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Enviar Email para Alunos"
        verbose_name_plural = "Enviar Email para Alunos"

    def __str__(self):
        return "Email para alunos do curso: {}".format(self.course.name)
