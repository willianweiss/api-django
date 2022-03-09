from http import HTTPStatus

from rest_framework.exceptions import APIException

from labqoda.helpers.drf.views import default_exception_handler


class FakeError(APIException):
    status_code = HTTPStatus.CONFLICT
    default_detail = "An default detail"
    default_code = "my_error_code"


class TestCustomExceptionHandler:
    def test_should_include_error_code_on_response(self):
        response = default_exception_handler(FakeError(), None)

        assert response.data["error_code"] == "my_error_code"
        assert response.status_code == HTTPStatus.CONFLICT
