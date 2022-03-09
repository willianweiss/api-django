from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager

from .choices import APPROVED, DISAPPROVED, PENDING, STATUS


class Thread(models.Model):

    title = models.CharField("Título", max_length=100)
    slug = models.SlugField("Identificador", max_length=100)
    content = models.ForeignKey("courses.Content", on_delete=models.CASCADE)

    views = models.IntegerField("Visualizações", blank=True, default=0)
    answers = models.IntegerField("Respostas", blank=True, default=0)
    tags = TaggableManager()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("thread-detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Tópico"
        verbose_name_plural = "Tópicos"
        ordering = ["-updated"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Thread, self).save(*args, **kwargs)


class Reply(models.Model):
    PENDING = PENDING
    APPROVED = APPROVED
    DISAPPROVED = DISAPPROVED

    thread = models.ForeignKey(
        Thread,
        verbose_name="Tópico",
        related_name="replies",
        on_delete=models.CASCADE,
    )
    reply = models.TextField("Resposta")
    comment = models.ForeignKey(
        "Reply",
        blank=True,
        null=True,
        related_name="comments",
        on_delete=models.CASCADE,
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Autor(a)",
        related_name="replies",
        on_delete=models.CASCADE,
    )
    correct = models.BooleanField("Correta?", blank=True, default=False)
    status = models.PositiveIntegerField(choices=STATUS, default=PENDING)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reply[:100]

    class Meta:
        verbose_name = "Resposta"
        verbose_name_plural = "Respostas"
        ordering = ["-correct", "created"]


def post_save_reply(created, instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()
    if instance.correct:
        instance.thread.replies.exclude(pk=instance.pk).update(correct=False)


def post_delete_reply(instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()


models.signals.post_save.connect(
    post_save_reply, sender=Reply, dispatch_uid="post_save_reply"
)
models.signals.post_delete.connect(
    post_delete_reply, sender=Reply, dispatch_uid="post_delete_reply"
)
