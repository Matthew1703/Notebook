# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.default_api_base import BaseDefaultApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field, StrictInt, StrictStr
from typing import Any, Optional
from typing_extensions import Annotated
from openapi_server.models.create_contact_request import CreateContactRequest
from openapi_server.models.get_contact import GetContact
from openapi_server.models.get_contacts import GetContacts
from openapi_server.models.update_contact_request import UpdateContactRequest


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/api/contacts",
    responses={
        200: {"model": GetContacts, "description": "OK"},
        400: {"description": "Validation error"},
    },
    tags=["default"],
    summary="Получение всех контактов через пагинацию",
    response_model_by_alias=True,
)
async def get_contacts(
    page_size: Annotated[int, Field(le=1000, strict=True, ge=1, description="Paging")] = Query(None, description="Paging", alias="pageSize", ge=1, le=1000),
    page_token: Annotated[Optional[StrictStr], Field(description="Paging token (opaque string, may be JSON-serialized internally)")] = Query(None, description="Paging token (opaque string, may be JSON-serialized internally)", alias="pageToken"),
) -> GetContacts:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().get_contacts(page_size, page_token)


@router.post(
    "/api/contacts",
    responses={
        201: {"description": "Created"},
    },
    tags=["default"],
    summary="Создание контакта",
    response_model_by_alias=True,
)
async def post_contact(
    create_contact_request: CreateContactRequest = Body(None, description=""),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().post_contact(create_contact_request)


@router.get(
    "/api/contact/{id}",
    responses={
        200: {"model": GetContact, "description": "OK"},
        404: {"description": "Not Found"},
    },
    tags=["default"],
    summary="Получение конкретного контакта",
    response_model_by_alias=True,
)
async def get_contact(
    id: StrictInt = Path(..., description=""),
) -> GetContact:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().get_contact(id)


@router.put(
    "/api/contact/{id}",
    responses={
        200: {"description": "OK"},
        404: {"description": "Not Found"},
    },
    tags=["default"],
    summary="Полное изменение контакта",
    response_model_by_alias=True,
)
async def put_contact(
    id: StrictInt = Path(..., description=""),
    create_contact_request: CreateContactRequest = Body(None, description=""),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().put_contact(id, create_contact_request)


@router.patch(
    "/api/contact/{id}",
    responses={
        200: {"model": GetContact, "description": "OK"},
        404: {"description": "Not Found"},
    },
    tags=["default"],
    summary="Изменение контакта",
    response_model_by_alias=True,
)
async def patch_contact(
    id: StrictInt = Path(..., description=""),
    update_contact_request: UpdateContactRequest = Body(None, description=""),
) -> GetContact:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().patch_contact(id, update_contact_request)
