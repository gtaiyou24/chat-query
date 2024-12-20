from __future__ import annotations

from enum import Enum

from http import HTTPStatus
from typing import Callable

from slf4py import create_logger


logger = create_logger()


class ErrorLevel(Enum):
    WARN = ("WARN", logger.warning)
    ERROR = ("ERROR", logger.error)
    CRITICAL = ("CRITICAL", logger.critical)

    def __init__(self, level: str, logging: Callable[[str], None]):
        self.level = level
        self.__logging = logging

    def to_logger(self, error_code: ErrorCode, detail: str):
        msg = "[Code] {code} [Message] {message} [Detail] {detail}".format(
            code=error_code.name, message=error_code.message, detail=detail
        )
        self.__logging(msg)


class ErrorCode(Enum):
    COMMON_2001 = ("アクセス拒否", ErrorLevel.WARN, HTTPStatus.FORBIDDEN)

    # 認証コンテキスト
    LOGIN_BAD_CREDENTIALS = ("メールアドレスまたはパスワードが間違っています", ErrorLevel.WARN, HTTPStatus.UNAUTHORIZED)
    SESSION_DOES_NOT_FOUND = (
        "セッションが見つからない、もしくはすでに有効期限を過ぎています", ErrorLevel.ERROR, HTTPStatus.UNAUTHORIZED)
    USER_DOES_NOT_FOUND = ("該当ユーザーが見つかりません。", ErrorLevel.WARN, HTTPStatus.NOT_FOUND)
    USER_IS_NOT_VERIFIED = ("該当ユーザーの認証が完了していません。", ErrorLevel.WARN, HTTPStatus.FORBIDDEN)
    VALID_TOKEN_DOES_NOT_EXISTS = (
        "トークンが見つからない、もしくはすでに有効期限を過ぎています", ErrorLevel.ERROR, HTTPStatus.BAD_REQUEST)
    TENANT_DOES_NOT_FOUND = ("テナントが見つかりません。", ErrorLevel.ERROR, HTTPStatus.NOT_FOUND)

    def __init__(self, message: str, error_level: ErrorLevel, http_status: HTTPStatus):
        self.message = message
        self.error_level = error_level
        self.http_status = http_status

    def log(self, detail: str):
        self.error_level.to_logger(self, detail)
