from rest_framework.views import exception_handler, set_rollback


def default_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data["error_code"] = exc.default_code

    # Execute rollback in case of error in the database transaction.
    set_rollback()

    return response
