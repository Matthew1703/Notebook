# pylint: skip-file
"""Реализация API для работы с контактами.

Содержит бизнес-логику CRUD операций с контактами,
используя in-memory хранилище (словарь).
"""

# coding: utf-8
import logging
from typing import Dict, Optional

from fastapi import HTTPException

# Импорт метрик (wildcard-импорт отключен для pylint)
from metrics import (  # pylint: disable=wildcard-import
    business_contact_age_histogram,
    business_contact_views_total,
    business_contacts_created_total,
    business_contacts_patched_total,
    business_contacts_updated_total,
    business_contacts_views_total,
    update_db_size_gauge,
)
from openapi_server.apis.default_api_base import BaseDefaultApi
from openapi_server.models.create_contact_request import CreateContactRequest
from openapi_server.models.get_contact import GetContact
from openapi_server.models.get_contacts import GetContacts
from openapi_server.models.update_contact_request import UpdateContactRequest

logger = logging.getLogger()

# In-memory хранилище контактов
contacts_db: Dict[int, dict] = {}
_next_id = 1  # Переименовано в _next_id для UPPER_CASE


class MyApiImpl(BaseDefaultApi):
    """Реализация API для управления контактами."""

    async def get_contacts(
        self, page_size: int, page_token: Optional[str] = None
    ) -> GetContacts:
        """Возвращает список всех контактов."""
        # pylint: disable=unused-argument
        try:
            global contacts_db  # noqa: PLW0602
            business_contacts_views_total.inc()
            # Преобразуем словари в объекты GetContact
            contacts_list = [
                GetContact(
                    name=str(contact.get("name", "")),
                    number=str(contact.get("number", "")),
                    age=int(contact.get("age", 0)),
                    email=contact.get("email"),
                    city=contact.get("city"),
                    description=contact.get("description"),
                )
                for contact in contacts_db.values()
            ]
            return GetContacts(contacts=contacts_list)
        except Exception as err:
            logger.error("get_contacts error: %s", err)
            raise

    async def post_contact(self, create_contact_request: CreateContactRequest) -> None:
        """Создаёт новый контакт."""
        try:
            global contacts_db, _next_id  # noqa: PLW0602
            business_contacts_created_total.inc()
            if create_contact_request.age is not None:
                business_contact_age_histogram.observe(create_contact_request.age)
            new_id = _next_id
            _next_id += 1
            contacts_db[new_id] = {
                "id": new_id,
                "name": create_contact_request.name,
                "number": create_contact_request.number,
                "age": create_contact_request.age,
                "email": create_contact_request.email,
                "city": create_contact_request.city,
                "description": create_contact_request.description,
            }
            update_db_size_gauge(len(contacts_db))
            return None
        except Exception as err:
            logger.error("post_contact error: %s", err)
            raise

    async def get_contact(self, contact_id: int) -> GetContact:
        """Возвращает контакт по ID."""
        try:
            global contacts_db  # noqa: PLW0602
            business_contact_views_total.inc()
            if contact_id not in contacts_db:
                raise HTTPException(status_code=404, detail="Contact not found")
            contact = contacts_db[contact_id]
            return GetContact(
                name=str(contact.get("name", "")),
                number=str(contact.get("number", "")),
                age=int(contact.get("age", 0)),
                email=contact.get("email"),
                city=contact.get("city"),
                description=contact.get("description"),
            )
        except Exception as err:
            logger.error("get_contact error for id %d: %s", contact_id, err)
            raise

    async def put_contact(
        self, contact_id: int, create_contact_request: CreateContactRequest
    ) -> None:
        """Полностью обновляет существующий контакт."""
        try:
            global contacts_db  # noqa: PLW0602
            business_contacts_updated_total.inc()
            if contact_id not in contacts_db:
                raise HTTPException(status_code=404, detail="Contact not found")
            contacts_db[contact_id] = {
                "id": contact_id,
                "name": create_contact_request.name,
                "number": create_contact_request.number,
                "age": create_contact_request.age,
                "email": create_contact_request.email,
                "city": create_contact_request.city,
                "description": create_contact_request.description,
            }
            return None
        except Exception as err:
            logger.error("put_contact error for id %d: %s", contact_id, err)
            raise

    async def patch_contact(
        self, contact_id: int, update_contact_request: UpdateContactRequest
    ) -> GetContact:
        """Частично обновляет существующий контакт."""
        try:
            global contacts_db  # noqa: PLW0602
            business_contacts_patched_total.inc()
            if contact_id not in contacts_db:
                raise HTTPException(status_code=404, detail="Contact not found")
            contact = contacts_db[contact_id]
            if update_contact_request.name is not None:
                contact["name"] = update_contact_request.name
            if update_contact_request.number is not None:
                contact["number"] = update_contact_request.number
            if update_contact_request.age is not None:
                contact["age"] = update_contact_request.age
            if update_contact_request.email is not None:
                contact["email"] = update_contact_request.email
            if update_contact_request.city is not None:
                contact["city"] = update_contact_request.city
            if update_contact_request.description is not None:
                contact["description"] = update_contact_request.description
            contacts_db[contact_id] = contact
            return GetContact(
                name=str(contact.get("name", "")),
                number=str(contact.get("number", "")),
                age=int(contact.get("age", 0)),
                email=contact.get("email"),
                city=contact.get("city"),
                description=contact.get("description"),
            )
        except Exception as err:
            logger.error("patch_contact error for id %d: %s", contact_id, err)
            raise
