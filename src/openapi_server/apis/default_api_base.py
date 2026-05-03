# coding: utf-8

from typing import Any, ClassVar, Dict, List, Optional, Tuple  # noqa: F401

from pydantic import Field, StrictInt, StrictStr
from typing_extensions import Annotated

from openapi_server.models.create_contact_request import CreateContactRequest
from openapi_server.models.get_contact import GetContact
from openapi_server.models.get_contacts import GetContacts
from openapi_server.models.update_contact_request import UpdateContactRequest


class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
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
        raise NotImplementedError

    async def post_contact(
        self,
        create_contact_request: CreateContactRequest,
    ) -> None: 
        raise NotImplementedError

    async def get_contact(
        self,
        id: StrictInt,
    ) -> GetContact: 
        raise NotImplementedError

    async def put_contact(
        self,
        id: StrictInt,
        create_contact_request: CreateContactRequest,
    ) -> None: 
        raise NotImplementedError

    async def patch_contact(
        self,
        id: StrictInt,
        update_contact_request: UpdateContactRequest,
    ) -> GetContact: 
        raise NotImplementedError
