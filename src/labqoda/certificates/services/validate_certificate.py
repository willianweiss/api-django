from labqoda.enrollments.models import CourseProgress, PathProgress


class ValidateCertificateService:
    @classmethod
    def validate_course_code(cls, code, user):
        course_progress = CourseProgress.objects.filter(
            status=CourseProgress.FINISHED, code=code, user=user
        ).last()
        if not course_progress:
            raise ValueError("Invalid Certificate Code")
        return course_progress

    @classmethod
    def validate_path_code(cls, code, user):
        path_progress = PathProgress.objects.filter(
            status=CourseProgress.FINISHED, code=code, user=user
        ).last()
        if not path_progress:
            raise ValueError("Invalid Certificate Code")
        return path_progress

    @classmethod
    def validate_path_or_code_certificate(cls, code):
        course_progress = CourseProgress.objects.filter(
            status=CourseProgress.FINISHED, code=code
        ).last()
        if course_progress:
            return "course", course_progress

        path_progress = PathProgress.objects.filter(
            status=CourseProgress.FINISHED, code=code
        ).last()
        if path_progress:
            return "path", path_progress

        raise ValueError("The certificate code does not exist")
