# coding: utf-8
import logging
from typing import Optional
from fastapi import HTTPException
from openapi_server.apis.default_api_base import BaseDefaultApi
from openapi_server.models.create_contact_request import CreateContactRequest
from openapi_server.models.get_contact import GetContact
from openapi_server.models.get_contacts import GetContacts
from openapi_server.models.update_contact_request import UpdateContactRequest
from metrics import (
    business_contacts_views_total,
    business_contacts_created_total,
    business_contact_age_histogram,
    business_contact_views_total,
    business_contacts_updated_total,
    business_contacts_patched_total,
    update_db_size_gauge
)

logger = logging.getLogger(__name__)

contacts_db = {}
next_id = 1

class MyApiImpl(BaseDefaultApi):

    async def get_contacts(self, page_size: int, page_token: Optional[str] = None) -> GetContacts:
        try:
            global contacts_db
            business_contacts_views_total.inc()
            contacts_list = list(contacts_db.values())
            return GetContacts(contacts=contacts_list, page_token=None)
        except Exception as e:
            logger.error(f"get_contacts error: {e}", exc_info=True)
            raise

    async def post_contact(self, create_contact_request: CreateContactRequest) -> None:
        try:
            global contacts_db, next_id
            business_contacts_created_total.inc()
            if create_contact_request.age is not None:
                business_contact_age_histogram.observe(create_contact_request.age)
            new_id = next_id
            next_id += 1
            contacts_db[new_id] = {
                "id": new_id,
                "name": create_contact_request.name,
                "number": create_contact_request.number,
                "age": create_contact_request.age,
                "email": create_contact_request.email,
                "city": create_contact_request.city,
                "description": create_contact_request.description
            }
            update_db_size_gauge(len(contacts_db))
            return None
        except Exception as e:
            logger.error(f"post_contact error: {e}", exc_info=True)
            raise

    async def get_contact(self, id: int) -> GetContact:
        try:
            global contacts_db
            business_contact_views_total.inc()
            if id not in contacts_db:
                raise HTTPException(status_code=404, detail="Contact not found")
            contact = contacts_db[id]
            return GetContact(
                name=contact["name"],
                number=contact["number"],
                age=contact["age"],
                email=contact.get("email"),
                city=contact.get("city"),
                description=contact.get("description")
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"get_contact error for id {id}: {e}", exc_info=True)
            raise

    async def put_contact(self, id: int, create_contact_request: CreateContactRequest) -> None:
        try:
            global contacts_db
            business_contacts_updated_total.inc()
            if id not in contacts_db:
                raise HTTPException(status_code=404, detail="Contact not found")
            contacts_db[id] = {
                "id": id,
                "name": create_contact_request.name,
                "number": create_contact_request.number,
                "age": create_contact_request.age,
                "email": create_contact_request.email,
                "city": create_contact_request.city,
                "description": create_contact_request.description
            }
            return None
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"put_contact error for id {id}: {e}", exc_info=True)
            raise

    async def patch_contact(self, id: int, update_contact_request: UpdateContactRequest) -> GetContact:
        try:
            global contacts_db
            business_contacts_patched_total.inc()
            if id not in contacts_db:
                raise HTTPException(status_code=404, detail="Contact not found")
            contact = contacts_db[id]
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
            contacts_db[id] = contact
            return GetContact(
                name=contact["name"],
                number=contact["number"],
                age=contact["age"],
                email=contact.get("email"),
                city=contact.get("city"),
                description=contact.get("description")
            )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"patch_contact error for id {id}: {e}", exc_info=True)
            raise