"""API эндпоинты для работы с контактами.

Содержит роутеры и обработчики HTTP запросов:
- GET /api/contacts - получение списка контактов
- POST /api/contacts - создание контакта
- GET /api/contact/{id} - получение контакта по ID
- PUT /api/contact/{id} - полное обновление контакта
- PATCH /api/contact/{id} - частичное обновление контакта
"""

# coding: utf-8
# pylint: skip-file

import importlib
import logging
import pkgutil
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, Path, Query, Request  # noqa: F401
from pydantic import Field, StrictInt, StrictStr
from typing_extensions import Annotated

import openapi_server.impl
from openapi_server.apis.default_api_base import BaseDefaultApi
from openapi_server.models.create_contact_request import CreateContactRequest
from openapi_server.models.get_contact import GetContact
from openapi_server.models.get_contacts import GetContacts
from openapi_server.models.update_contact_request import UpdateContactRequest

router = APIRouter()

# Динамическая загрузка реализаций API
impl_pkg = openapi_server.impl

for _, name, _ in pkgutil.iter_modules(impl_pkg.__path__, impl_pkg.__name__ + "."):  # type: ignore
    importlib.import_module(name)

logger = logging.getLogger(__name__)


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
    request: Request,
    page_size: Annotated[
        int, Field(le=1000, strict=True, ge=1, description="Paging")
    ] = Query(None, description="Paging", alias="pageSize", ge=1, le=1000),
    page_token: Annotated[
        Optional[StrictStr],
        Field(
            description="Paging token (opaque string, may be JSON-serialized internally)"
        ),
    ] = Query(
        None,
        description="Paging token (opaque string, may be JSON-serialized internally)",
        alias="pageToken",
    ),
) -> GetContacts:
    """Получение списка контактов с пагинацией."""
    logger.info(
        "Request path: %s, request method: %s", request.url.path, request.method
    )
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
    request: Request,
    create_contact_request: CreateContactRequest = Body(None, description=""),
) -> None:
    """Создание нового контакта."""
    logger.info(
        "Request path: %s, request method: %s", request.url.path, request.method
    )
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().post_contact(create_contact_request)


@router.get(
    "/api/contact/{contact_id}",
    responses={
        200: {"model": GetContact, "description": "OK"},
        404: {"description": "Not Found"},
    },
    tags=["default"],
    summary="Получение конкретного контакта",
    response_model_by_alias=True,
)
async def get_contact(
    request: Request,
    contact_id: StrictInt = Path(..., description=""),
) -> GetContact:
    """Получение контакта по ID."""
    logger.info(
        "Request path: %s, request method: %s", request.url.path, request.method
    )
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().get_contact(contact_id)


@router.put(
    "/api/contact/{contact_id}",
    responses={
        200: {"description": "OK"},
        404: {"description": "Not Found"},
    },
    tags=["default"],
    summary="Полное изменение контакта",
    response_model_by_alias=True,
)
async def put_contact(
    request: Request,
    contact_id: StrictInt = Path(..., description=""),
    create_contact_request: CreateContactRequest = Body(None, description=""),
) -> None:
    """Полное обновление существующего контакта."""
    logger.info(
        "Request path: %s, request method: %s", request.url.path, request.method
    )
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().put_contact(
        contact_id, create_contact_request
    )


@router.patch(
    "/api/contact/{contact_id}",
    responses={
        200: {"model": GetContact, "description": "OK"},
        404: {"description": "Not Found"},
    },
    tags=["default"],
    summary="Изменение контакта",
    response_model_by_alias=True,
)
async def patch_contact(
    request: Request,
    contact_id: StrictInt = Path(..., description=""),
    update_contact_request: UpdateContactRequest = Body(None, description=""),
) -> GetContact:
    """Частичное обновление существующего контакта."""
    logger.info(
        "Request path: %s, request method: %s", request.url.path, request.method
    )
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().patch_contact(
        contact_id, update_contact_request
    )
