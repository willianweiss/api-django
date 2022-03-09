import pytest
from model_bakery import baker


@pytest.fixture
def course_factory():
    return baker.make("courses.Course")


@pytest.fixture
def courses_factory():
    return baker.make("courses.Course", _quantity=10)


@pytest.fixture
def subject_factory():
    return baker.make("courses.Subject")


@pytest.fixture
def path_factory():
    return baker.make("courses.Path")


@pytest.fixture
def paths_factory():
    return baker.make("courses.Path", _quantity=10)


@pytest.fixture
def path_course_factory():
    return baker.make("courses.PathCourse")


@pytest.fixture
def paths_courses_factory(paths_factory, course_factory):
    return baker.make("courses.PathCourse", _quantity=10,)


@pytest.fixture
def module_factory():
    return baker.make("courses.Module")


@pytest.fixture
def modules_factory(paths_factory, course_factory):
    return baker.make("courses.Module", _quantity=10,)


@pytest.fixture
def content_factory():
    return baker.make("courses.Content")


@pytest.fixture
def contents_factory():
    return baker.make("courses.Content", _quantity=10)


@pytest.fixture
def item_code_factory():
    return baker.make("courses.Code")


@pytest.fixture
def course_payload(user_factory, subject_factory):
    return {
        "name": "Curso Python",
        "slug": "curso-python",
        "description": "Python eh top",
        "minidesc": "Python eh top ate na lua",
        "startDate": "2020-08-22",
        "image": "string",
        "duration": "string",
        "priceTotal": "string",
        "priceActual": "string",
        "req1": "string",
        "re2": "string",
        "req3": "string",
        "req4": "string",
        "req5": "string",
        "instructor": user_factory.pk,
        "subject": subject_factory.pk,
    }


@pytest.fixture
def module_payload():
    return {
        "title": "Testes com Pytest",
        "description": "Apreenda testes em python com a lib pytest",
        "tags": "test",
    }


@pytest.fixture
def content_payload():
    return {
        "title": "Instalando Pytest",
        "description": "Use Linux!!!",
        "duration": "10 minutos",
    }
