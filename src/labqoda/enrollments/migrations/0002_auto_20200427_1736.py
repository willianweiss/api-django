# Generated by Django 3.0.1 on 2020-04-27 20:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('enrollments', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0002_auto_20200427_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='pathprogress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='usuário'),
        ),
        migrations.AddField(
            model_name='pathenrollment',
            name='enrollment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='enrollments.Enrollment'),
        ),
        migrations.AddField(
            model_name='pathenrollment',
            name='path',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='courses.Path', verbose_name='Path'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='usuário'),
        ),
        migrations.AddField(
            model_name='coursewatchedcontent',
            name='content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Content', verbose_name='Content'),
        ),
        migrations.AddField(
            model_name='coursewatchedcontent',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='coursewatchedcontent',
            name='course_progress',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enrollments.CourseProgress', verbose_name='Curso'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='coursewatchedcontent',
            order_with_respect_to='updated',
        ),
        migrations.AddField(
            model_name='courseprogress',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='Curso'),
        ),
        migrations.AddField(
            model_name='courseprogress',
            name='course_enrollment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='enrollments.CourseEnrollment'),
        ),
        migrations.AddField(
            model_name='courseprogress',
            name='path_enrollment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='enrollments.PathEnrollment'),
        ),
        migrations.AddField(
            model_name='courseprogress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='usuário'),
        ),
        migrations.AddField(
            model_name='courseenrollment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='Curso'),
        ),
        migrations.AddField(
            model_name='courseenrollment',
            name='enrollment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enrollments.Enrollment'),
        ),
        migrations.AlterUniqueTogether(
            name='pathprogress',
            unique_together={('enrollment', 'path')},
        ),
        migrations.AlterUniqueTogether(
            name='pathenrollment',
            unique_together={('enrollment', 'path')},
        ),
        migrations.AlterUniqueTogether(
            name='coursewatchedcontent',
            unique_together={('course_progress', 'item_type', 'object_id', 'content')},
        ),
        migrations.AlterUniqueTogether(
            name='courseenrollment',
            unique_together={('enrollment', 'course')},
        ),
    ]
