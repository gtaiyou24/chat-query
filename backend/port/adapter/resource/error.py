from http import HTTPStatus

from pydantic import BaseModel


class ErrorJson(BaseModel):
    type: str
    title: str
    status: HTTPStatus
    instance: str

