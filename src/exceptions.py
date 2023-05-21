from fastapi import HTTPException
from starlette import status


class BaseHTTPException(HTTPException):
    detail = "Bad request"
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class NotFoundHTTPException(BaseHTTPException):
    detail = "Not found"
    status_code = status.HTTP_404_NOT_FOUND
