"""Модель UpdateContactRequest для API.

Содержит поля для частичного обновления контакта:
- name: имя (опционально)
- number: номер телефона (опционально, 11 цифр)
- age: возраст (опционально, 0-150 лет)
- email: электронная почта (опционально)
- city: город (опционально)
- description: описание (опционально)
"""

# coding: utf-8

from __future__ import annotations

import json
import pprint
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, StrictStr
from typing_extensions import Annotated

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class UpdateContactRequest(BaseModel):
    """Модель запроса для частичного обновления контакта."""

    name: Optional[StrictStr] = None
    number: Optional[
        Annotated[str, Field(min_length=11, strict=True, max_length=11)]
    ] = None
    age: Optional[Annotated[int, Field(le=150, strict=True, ge=0)]] = None
    email: Optional[StrictStr] = None
    city: Optional[StrictStr] = None
    description: Optional[StrictStr] = None

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
        """Create an instance of UpdateContactRequest from a JSON string."""
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
        # set to None if description (nullable) is None
        # and model_fields_set contains the field
        if self.description is None and "description" in self.model_fields_set:
            _dict["description"] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of UpdateContactRequest from a dict."""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "name": obj.get("name"),
                "number": obj.get("number"),
                "age": obj.get("age"),
                "email": obj.get("email"),
                "city": obj.get("city"),
                "description": obj.get("description"),
            }
        )
        return _obj
