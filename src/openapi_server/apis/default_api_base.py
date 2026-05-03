# pylint: skip-file
"""Базовый абстрактный класс для API эндпоинтов контактов.

Содержит абстрактные методы для CRUD операций:
- get_contacts: получение списка контактов
- post_contact: создание контакта
- get_contact: получение одного контакта
- put_contact: полное обновление контакта
- patch_contact: частичное обновление контакта
"""

# coding: utf-8

from typing import ClassVar, Optional, Tuple  # noqa: F401

from pydantic import Field, StrictInt, StrictStr
from typing_extensions import Annotated

from openapi_server.models.create_contact_request import CreateContactRequest
from openapi_server.models.get_contact import GetContact
from openapi_server.models.get_contacts import GetContacts
from openapi_server.models.update_contact_request import UpdateContactRequest


class BaseDefaultApi:
    """Базовый абстрактный класс для API.

    Содержит методы, которые должны быть реализованы в дочерних классах.
    """

    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        """Регистрирует подкласс при наследовании."""
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)

    async def get_contacts(
        self,
        page_size: Annotated[
            int, Field(le=1000, strict=True, ge=1, description="Paging")
        ],
        page_token: Annotated[
            Optional[StrictStr],
            Field(
                description="Paging token (opaque string, may be JSON-serialized internally)"
            ),
        ],
    ) -> GetContacts:
        """Получение списка контактов с пагинацией.

        Args:
            page_size: Количество элементов на странице (1-1000).
            page_token: Токен для пагинации.

        Returns:
            Объект GetContacts со списком контактов.
        """
        raise NotImplementedError

    async def post_contact(
        self,
        create_contact_request: CreateContactRequest,
    ) -> None:
        """Создание нового контакта.

        Args:
            create_contact_request: Данные для создания контакта.

        Returns:
            None при успешном создании.
        """
        raise NotImplementedError

    async def get_contact(
        self,
        contact_id: StrictInt,
    ) -> GetContact:
        """Получение контакта по ID.

        Args:
            contact_id: Уникальный идентификатор контакта.

        Returns:
            Объект GetContact с данными контакта.
        """
        raise NotImplementedError

    async def put_contact(
        self,
        contact_id: StrictInt,
        create_contact_request: CreateContactRequest,
    ) -> None:
        """Полное обновление существующего контакта.

        Args:
            contact_id: Уникальный идентификатор контакта.
            create_contact_request: Новые данные для контакта.

        Returns:
            None при успешном обновлении.
        """
        raise NotImplementedError

    async def patch_contact(
        self,
        contact_id: StrictInt,
        update_contact_request: UpdateContactRequest,
    ) -> GetContact:
        """Частичное обновление существующего контакта.

        Args:
            contact_id: Уникальный идентификатор контакта.
            update_contact_request: Данные для частичного обновления.

        Returns:
            Обновлённый объект GetContact.
        """
        raise NotImplementedError
