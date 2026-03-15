from openapi_server.apis.default_api_base import BaseDefaultApi
from openapi_server.models.get_contacts import GetContacts
from openapi_server.models.get_contact import GetContact
from openapi_server.models.create_contact_request import CreateContactRequest
from openapi_server.models.update_contact_request import UpdateContactRequest
from typing import Optional
import json

# Временное хранилище в памяти (пока без БД)
contacts_db = {}
next_id = 1

class MyApiImpl(BaseDefaultApi):
    
    async def get_contacts(self, page_size: int, page_token: Optional[str] = None) -> GetContacts:
        """Получить все контакты"""
        global contacts_db
        # Преобразуем словарь в список для ответа
        contacts_list = list(contacts_db.values())
        return GetContacts(contacts=contacts_list, page_token=None)
    
    async def post_contact(self, create_contact_request: CreateContactRequest) -> None:
        """Создать новый контакт"""
        global contacts_db, next_id
        
        # Создаём контакт с новым ID
        new_id = next_id
        next_id += 1
        
        # Сохраняем
        contacts_db[new_id] = {
            "id": new_id,
            "name": create_contact_request.name,
            "number": create_contact_request.number,
            "age": create_contact_request.age,
            "email": create_contact_request.email,
            "city": create_contact_request.city,
            "description": create_contact_request.description
        }
        
        # В реальном проекте здесь нужно вернуть 201 с Location
        return None
    
    async def get_contact(self, id: int) -> GetContact:
        """Получить контакт по ID"""
        global contacts_db
        
        if id not in contacts_db:
            # FastAPI преобразует это в 404
            from fastapi import HTTPException
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
    
    async def put_contact(self, id: int, create_contact_request: CreateContactRequest) -> None:
        """Полное обновление контакта"""
        global contacts_db
        
        if id not in contacts_db:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Contact not found")
        
        # Полностью заменяем контакт
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
    
    async def patch_contact(self, id: int, update_contact_request: UpdateContactRequest) -> GetContact:
        """Частичное обновление контакта"""
        global contacts_db
        
        if id not in contacts_db:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Contact not found")
        
        contact = contacts_db[id]
        
        # Обновляем только переданные поля
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