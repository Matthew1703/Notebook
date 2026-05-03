"""Модель GetContacts для API.

Содержит список контактов и токен пагинации:
- contacts: список объектов GetContact (может быть пустым)
- page_token: токен для следующей страницы (опционально)
"""

# coding: utf-8

from __future__ import annotations

import json
import pprint
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, StrictStr

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


# Отложенный импорт для избежания циклических зависимостей
def _get_contact_model():
    from openapi_server.models.get_contact import GetContact

    return GetContact


class GetContacts(BaseModel):
    """Модель ответа со списком контактов."""

    contacts: List = Field(default_factory=list)
    page_token: Optional[StrictStr] = Field(default=None, alias="pageToken")

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }

    def to_str(self) -> str:
        """Returns the string representation of the model using alias."""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias."""
        # pydantic v2: model_dump_json with by_alias=True and exclude_unset=True
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of GetContacts from a JSON string."""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={},
            exclude_none=True,
        )
        # override the default output from pydantic by calling
        # `to_dict()` of each item in contacts (list)
        if self.contacts and isinstance(self.contacts, list):
            _items = []
            for _item in self.contacts:
                if hasattr(_item, "to_dict"):
                    _items.append(_item.to_dict())
                else:
                    _items.append(_item)
            _dict["contacts"] = _items
        # set to None if page_token (nullable) is None
        # and model_fields_set contains the field
        if self.page_token is None and "page_token" in self.model_fields_set:
            _dict["pageToken"] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of GetContacts from a dict."""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        # Получаем модель GetContact для преобразования
        GetContact = _get_contact_model()

        _obj = cls.model_validate(
            {
                "contacts": [
                    GetContact.from_dict(_item) for _item in (obj.get("contacts") or [])
                ]
                or None,
                "pageToken": obj.get("pageToken"),
            }
        )
        return _obj
