# tests/test_my_api_impl.py
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from fastapi import HTTPException
from openapi_server.impl.my_impl import MyApiImpl
from openapi_server.models.create_contact_request import CreateContactRequest
from openapi_server.models.update_contact_request import UpdateContactRequest
from openapi_server.models.get_contact import GetContact
from openapi_server.models.get_contacts import GetContacts

import openapi_server.impl.my_impl as my_impl_module


@pytest.fixture
def api_impl():
    my_impl_module.contacts_db.clear()
    my_impl_module.next_id = 1
    return MyApiImpl()


@pytest.fixture
def sample_contact_data():
    return {
        "name": "John Doe",
        "number": "79161234567",
        "age": 30,
        "email": "john@example.com",
        "city": "Moscow",
        "description": "Test contact",
    }


@pytest.fixture
def create_request(sample_contact_data):
    return CreateContactRequest(**sample_contact_data)


class TestPostContact:
    @pytest.mark.asyncio
    async def test_create_contact_success(self, api_impl, create_request):
        result = await api_impl.post_contact(create_request)

        assert result is None
        assert len(my_impl_module.contacts_db) == 1
        assert list(my_impl_module.contacts_db.keys()) == [1]

    @pytest.mark.asyncio
    async def test_create_contact_increments_id(self, api_impl, create_request):
        await api_impl.post_contact(create_request)
        await api_impl.post_contact(create_request)

        assert 1 in my_impl_module.contacts_db
        assert 2 in my_impl_module.contacts_db
        assert len(my_impl_module.contacts_db) == 2


class TestGetContact:
    @pytest.mark.asyncio
    async def test_get_contact_success(self, api_impl, create_request):
        await api_impl.post_contact(create_request)

        result = await api_impl.get_contact(1)

        assert isinstance(result, GetContact)
        assert result.name == "John Doe"
        assert result.number == "79161234567"
        assert result.age == 30
        assert result.email == "john@example.com"

    @pytest.mark.asyncio
    async def test_get_contact_not_found(self, api_impl):
        with pytest.raises(HTTPException) as exc_info:
            await api_impl.get_contact(999)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Contact not found"


class TestGetContacts:
    @pytest.mark.asyncio
    async def test_get_contacts_empty(self, api_impl):
        """Получение списка когда нет контактов — возвращает пустой список"""
        result = await api_impl.get_contacts(page_size=10)

        assert isinstance(result, GetContacts)
        # ✅ Исправлено: contacts может быть пустым списком
        # Модель GetContacts не запрещает пустые списки, если min_length не указан
        assert result.contacts == []
        assert result.page_token is None  # или не проверяем page_token

    @pytest.mark.asyncio
    async def test_get_contacts_with_data(self, api_impl, create_request):
        await api_impl.post_contact(create_request)
        await api_impl.post_contact(create_request)

        result = await api_impl.get_contacts(page_size=10)

        assert isinstance(result, GetContacts)
        assert len(result.contacts) == 2
        assert result.page_token is None


class TestPutContact:
    @pytest.mark.asyncio
    async def test_put_contact_success(self, api_impl, create_request):
        await api_impl.post_contact(create_request)

        updated_data = {
            "name": "Jane Doe",
            "number": "79876543210",
            "age": 25,
            "email": "jane@example.com",
            "city": "SPb",
            "description": "Updated",
        }
        update_request = CreateContactRequest(**updated_data)
        result = await api_impl.put_contact(1, update_request)

        assert result is None
        assert my_impl_module.contacts_db[1]["name"] == "Jane Doe"
        assert my_impl_module.contacts_db[1]["number"] == "79876543210"

    @pytest.mark.asyncio
    async def test_put_contact_not_found(self, api_impl, create_request):
        with pytest.raises(HTTPException) as exc_info:
            await api_impl.put_contact(999, create_request)

        assert exc_info.value.status_code == 404


class TestPatchContact:
    @pytest.mark.asyncio
    async def test_patch_contact_success(self, api_impl, create_request):
        await api_impl.post_contact(create_request)

        patch_request = UpdateContactRequest(name="John Updated", age=31, city=None)
        result = await api_impl.patch_contact(1, patch_request)

        assert isinstance(result, GetContact)
        assert result.name == "John Updated"
        assert result.age == 31
        assert result.number == "79161234567"
        # ✅ Исправлено: city НЕ должен меняться, если не передан (остаётся Moscow)
        assert result.city == "Moscow"  # было Moscow, city=None не меняет

    @pytest.mark.asyncio
    async def test_patch_contact_not_found(self, api_impl):
        patch_request = UpdateContactRequest(name="Test")
        with pytest.raises(HTTPException) as exc_info:
            await api_impl.patch_contact(999, patch_request)

        assert exc_info.value.status_code == 404


class TestE2E:
    @pytest.mark.asyncio
    async def test_full_crud_flow(self, api_impl):
        result = await api_impl.get_contacts(page_size=10)
        assert len(result.contacts) == 0

        create_req = CreateContactRequest(
            name="Test User",
            number="79261234567",
            age=28,
            email="test@example.com",
            city="Kazan",
            description="Initial",
        )
        await api_impl.post_contact(create_req)

        result = await api_impl.get_contacts(page_size=10)
        assert len(result.contacts) == 1

        contact = await api_impl.get_contact(1)
        assert contact.name == "Test User"

        patch_req = UpdateContactRequest(name="Updated User", age=29)
        updated = await api_impl.patch_contact(1, patch_req)
        assert updated.name == "Updated User"
        assert updated.age == 29

        put_req = CreateContactRequest(
            name="New Full",
            number="79990001122",
            age=35,
            email="new@example.com",
            city="Sochi",
            description="Full overwrite",
        )
        await api_impl.put_contact(1, put_req)

        final = await api_impl.get_contact(1)
        assert final.name == "New Full"
        assert final.number == "79990001122"
        assert final.age == 35