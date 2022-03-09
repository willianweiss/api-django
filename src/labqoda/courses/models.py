import os

from django.contrib.auth import get_user_model
from django.db import models
from taggit.managers import TaggableManager
from tinymce.models import HTMLField

from .fields import OrderField
from .services.vdocipher import VdoCipher

User = get_user_model()


class Subject(models.Model):

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["title"]

    def __str__(self):
        return self.title


# Course(N modules) generate 1 certificate at the end
class Course(models.Model):
    instructor = models.ForeignKey(
        User, related_name="courses_created", on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject,
        related_name="courses",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    name = models.CharField("Nome", max_length=100)
    slug = models.SlugField("Slug")
    description = models.TextField("Descrição", blank=True)
    minidesc = models.CharField("Mini Descrição", max_length=325, blank=True)
    start_date = models.DateField("Data de início", null=True, blank=True)
    image = models.ImageField(
        upload_to="courses/images",
        verbose_name="Imagem",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)
    tags = TaggableManager(blank=True)
    duration = models.TextField(default="", null=True, blank=True)  # in hours
    price_total = models.TextField(default="992")
    price_actual = models.TextField(default="992")
    # requisites for course
    req1 = models.TextField(blank=True)
    re2 = models.TextField(blank=True)
    req3 = models.TextField(blank=True)
    req4 = models.TextField(blank=True)
    req5 = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/courses/" + self.slug

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["-created_at"]


# Module (N contents)
class Module(models.Model):
    course = models.ForeignKey(
        Course, related_name="modules", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    tags = TaggableManager(blank=True)
    order = OrderField(blank=True, for_fields=["course"])

    class Meta:
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"
        ordering = ["order"]

    def __str__(self):
        return "{}. {}. ({})".format(self.order, self.title, self.course)


# Content/lesson
class Content(models.Model):
    module = models.ForeignKey(
        Module, related_name="contents", on_delete=models.CASCADE
    )
    order = OrderField(blank=True, for_fields=["module"])
    duration = models.CharField(
        max_length=200, default="", null=True, blank=True
    )
    title = models.CharField(max_length=250)
    instructor = models.ForeignKey(
        User, related_name="%(class)s_related", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Aula"
        verbose_name_plural = "Aulas"
        ordering = ["order"]

    def save(self, *args, **kwargs):
        obj = super(Content, self).save(*args, **kwargs)
        if not self.thread_set.all():
            self.thread_set.create(content=self, title=self.title)
        return obj

    def __str__(self):
        return f"Content: {self.order}, Module: {self.module}"


class ItemBase(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]
        abstract = True

    def __str__(self):
        return "self.order"


class Text(ItemBase):
    text = HTMLField()


class Code(ItemBase):
    code = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to="files")

    def get_filename(self):
        return os.path.basename(self.file.name)


class Image(ItemBase):
    image = models.FileField(upload_to="images")


class Video(ItemBase):
    videoid = models.CharField(max_length=150, default="", blank=True)

    def delete(self, *args, **kwargs):
        vdochiper = VdoCipher()
        vdochiper.delete(self.videoid)
        super(Video, self).delete(*args, **kwargs)


class Path(models.Model):
    tags = TaggableManager(blank=True)
    name = models.CharField("Nome", max_length=100)
    slug = models.SlugField("Slug")
    description = models.TextField("Descrição", blank=True)
    minidesc = models.CharField("Mini Descrição", max_length=325, blank=True)
    start_date = models.DateField("Data de início", null=True, blank=True)
    image = models.ImageField(
        upload_to="courses/images",
        verbose_name="Imagem",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)
    courses = models.ManyToManyField(
        Course, related_name="courses", through="PathCourse"
    )

    def __str__(self):
        return "{0}".format(self.name)


class PathCourse(models.Model):
    class Meta:
        unique_together = ("path", "course")
        ordering = ["order"]

    path = models.ForeignKey(Path, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return super().__str__()
