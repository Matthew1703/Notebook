"""Дополнительные модели для API аутентификации.

Содержит вспомогательные модели:
- TokenModel: модель для хранения данных токена
"""

# coding: utf-8

try:
    from pydantic import BaseModel
except ImportError:
    # Заглушка для случаев, когда pydantic не установлен
    class BaseModel:  # type: ignore
        """Fallback BaseModel when pydantic is not available."""

        # pylint: disable=too-few-public-methods
        __slots__ = ()


class TokenModel(BaseModel):  # pylint: disable=too-few-public-methods
    """Модель для хранения данных токена."""

    sub: str
