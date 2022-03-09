import datetime
import uuid

from django.conf import settings
from django.db import models

from labqoda.courses.models import Content, Course, Path


class Enrollment(models.Model):
    PENDENTE = 0
    APROVADO = 1
    CANCELADO = 2
    STATUS_CHOICES = (
        (PENDENTE, "Pendente"),
        (APROVADO, "Aprovado"),
        (CANCELADO, "Cancelado"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="usuário",
        on_delete=models.CASCADE,
    )
    code = models.UUIDField(
        "Codigo da inscrição", default=uuid.uuid4, editable=False
    )
    status = models.IntegerField(
        "Situação", choices=STATUS_CHOICES, default=PENDENTE
    )
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    def active(self):
        self.status = 1
        self.save()

    def is_approved(self):
        return self.status == 1

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "Inscrição"
        verbose_name_plural = "Inscrições"


class CourseEnrollment(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, verbose_name="Curso", on_delete=models.PROTECT
    )

    class Meta:
        unique_together = ("enrollment", "course")

    def __str__(self):
        return f"{self.course}: {self.enrollment}"


class PathEnrollment(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    path = models.ForeignKey(
        Path, verbose_name="Path", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.path}: {self.enrollment}"


class CourseProgress(models.Model):
    """GESTAO DE PROGRESSO"""

    QUEUED = 0
    STARTED = 1
    FINISHED = 2
    STATUS_CHOICES = (
        (QUEUED, "Queued"),
        (STARTED, "Started"),
        (FINISHED, "Finished"),
    )

    course_enrollment = models.ForeignKey(
        CourseEnrollment, on_delete=models.SET_NULL, null=True, blank=True
    )
    path_enrollment = models.ForeignKey(
        PathEnrollment, on_delete=models.SET_NULL, null=True, blank=True
    )
    code = models.UUIDField(
        "Codigo do curso", default=uuid.uuid4, editable=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="usuário",
        on_delete=models.SET_NULL,
        null=True,
    )
    course = models.ForeignKey(
        Course, verbose_name="Curso", null=True, on_delete=models.SET_NULL
    )
    status = models.IntegerField("Progress", choices=STATUS_CHOICES, default=0)
    date_of_issue = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Progresso no Curso"
        verbose_name_plural = "Progressos nos Cursos"

    def get_whatched_contents_ids(self):
        contents = self.coursewatchedcontent_set.values_list(
            "content__id", flat=True
        ).distinct()
        return contents

    def get_total_contents_course(self):
        modules = self.course.modules.all()

        contents_ids = []
        for module in modules:
            ids = module.contents.all().values_list("id").distinct()
            contents_ids += ids

        return len(contents_ids)

    def get_total_contents_watched_course(self):
        modules = self.course.modules.all()

        contents_ids = []
        for module in modules:
            ids = module.contents.all().values_list("id").distinct()
            contents_ids += ids

        return self.coursewatchedcontent_set.filter(
            content_id__in=contents_ids
        ).count()

    def set_started_status(self):
        if self.coursewatchedcontent_set.exists():
            self.status = CourseProgress.STARTED
            self.save()

    def set_finished_status(self):
        modules = self.course.modules.all()

        contents_ids = []
        for module in modules:
            ids = module.contents.all().values_list("id").distinct()
            contents_ids += ids

        contents_length = self.coursewatchedcontent_set.filter(
            content_id__in=contents_ids
        ).count()

        if len(contents_ids) == contents_length:
            self.status = self.FINISHED
            self.date_of_issue = datetime.datetime.now()
            self.save()

    def update_course_status(self):
        if self.status == CourseProgress.QUEUED:
            self.set_started_status()
        elif self.status == self.STARTED:
            self.set_finished_status()
        elif self.status == self.FINISHED:
            pass


class CourseWatchedContent(models.Model):

    # TODO: salvar apenas um por depois unique together
    course_progress = models.ForeignKey(
        CourseProgress, verbose_name="Curso", on_delete=models.CASCADE
    )
    content = models.ForeignKey(
        Content, verbose_name="Content", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        order_with_respect_to = "updated"
        unique_together = ("course_progress", "content")

    @classmethod
    def get_last_content_user_course(cls, course_id, user):
        return (
            CourseWatchedContent.objects.filter(
                course_progress__course_id=course_id,
                course_progress__user=user,
            )
            .order_by("updated")
            .last()
        )

    @classmethod
    def create_first_content_user_course(cls, course_id, user):
        has_contents = cls.objects.filter(
            course_progress__course_id=course_id, course_progress__user=user
        )

        if not has_contents:
            course_progress = CourseProgress.objects.filter(
                user=user, course_id=course_id
            ).last()

            module = (
                course_progress.course.modules.all().order_by("order").first()
            )
            content = module.contents.all().order_by("order").first()

            if content:
                (
                    created_content,
                    _,
                ) = CourseWatchedContent.objects.update_or_create(
                    course_progress=course_progress,
                    content=content,
                    defaults={
                        "course_progress": course_progress,
                        "content": content,
                    },
                )
                return created_content

    def save(self, *args, **kwargs):
        return super(CourseWatchedContent, self).save(*args, **kwargs)


class PathProgress(models.Model):

    QUEUED = 0
    STARTED = 1
    FINISHED = 2
    STATUS_CHOICES = (
        (QUEUED, "Queued"),
        (STARTED, "Started"),
        (FINISHED, "Finished"),
    )

    enrollment = models.OneToOneField(PathEnrollment, on_delete=models.CASCADE)
    code = models.UUIDField(
        "Codigo do curso", default=uuid.uuid4, editable=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="usuário",
        on_delete=models.CASCADE,
    )
    path = models.ForeignKey(
        Path, verbose_name="Path", on_delete=models.CASCADE
    )
    status = models.IntegerField("Progress", choices=STATUS_CHOICES, default=0)

    class Meta:
        verbose_name = "Progresso na Trilha"
        verbose_name_plural = "Progressos nas Trilhas"
        unique_together = ("enrollment", "path")

    def set_started_status(self):
        courses_ids = self.path.courses.all().values_list("id").distinct()
        finished_courses = CourseProgress.objects.filter(
            id__in=courses_ids, status=CourseProgress.FINISHED
        ).exists()

        if finished_courses:
            self.status = PathProgress.STARTED
            self.save()

    def set_finished_status(self):
        courses_ids = self.path.courses.all().values_list("id").distinct()
        finished_courses = CourseProgress.objects.filter(
            id__in=courses_ids, status=CourseProgress.FINISHED
        ).count()

        if finished_courses == len(courses_ids):
            self.status = PathProgress.FINISHED
            self.save()

    def update_pathprogress_status(self):
        if self.status == self.QUEUED:
            self.set_started_status()
        elif self.status == self.STARTED:
            self.set_finished_status()


def create_or_update_course_progress(instance):
    CourseProgress.objects.update_or_create(
        course=instance.course,
        user=instance.enrollment.user,
        defaults={"course_enrollment": instance},
    )


def create_or_update_course_progress_by_path(instance):
    for course in instance.path.courses.all():
        CourseProgress.objects.update_or_create(
            course=course,
            user=instance.enrollment.user,
            defaults={"path_enrollment": instance,},
        )

    if not hasattr(instance, "pathprogress"):
        PathProgress.objects.create(
            enrollment=instance,
            path=instance.path,
            user=instance.enrollment.user,
        )


def post_save_course_enrollment(created, instance, **kwargs):
    if created and instance.enrollment.status == Enrollment.APROVADO:
        create_or_update_course_progress(instance)


def post_save_path_enrollment(created, instance, **kwargs):
    if created and instance.enrollment.status == Enrollment.APROVADO:
        create_or_update_course_progress_by_path(instance)


def post_save_enrollment(created, instance, **kwargs):
    if instance.status == Enrollment.APROVADO:
        course_enrollment = instance.courseenrollment_set.first()
        path_enrollment = instance.pathenrollment_set.first()
        if course_enrollment:
            create_or_update_course_progress(course_enrollment)
        elif path_enrollment:
            create_or_update_course_progress_by_path(path_enrollment)
        else:
            raise ValueError("É necessario cadastrar curso ou path")


models.signals.post_save.connect(
    post_save_course_enrollment,
    sender=CourseEnrollment,
    dispatch_uid="post_save_course_enrollment",
)
models.signals.post_save.connect(
    post_save_path_enrollment,
    sender=PathEnrollment,
    dispatch_uid="post_save_path_enrollment",
)
models.signals.post_save.connect(
    post_save_enrollment,
    sender=Enrollment,
    dispatch_uid="post_save_enrollment",
)
