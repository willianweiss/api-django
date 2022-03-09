from model_bakery.recipe import Recipe, foreign_key

from labqoda.courses.models import Course
from labqoda.enrollments.models import (
    CourseEnrollment,
    CourseProgress,
    Enrollment,
    PathEnrollment,
)

course = Recipe(Course)

enrollment = Recipe(Enrollment, status=Enrollment.PENDENTE)

course_enrollment = Recipe(CourseEnrollment,)

path_enrollment = Recipe(PathEnrollment,)

course_progress = Recipe(
    CourseProgress,
    course_enrollment=foreign_key(course_enrollment),
    path_enrollment=foreign_key(path_enrollment),
    status=CourseProgress.STARTED,
    course=course,
)
