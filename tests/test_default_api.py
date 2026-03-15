# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictInt, StrictStr  # noqa: F401
from typing import Any, Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.create_contact_request import CreateContactRequest  # noqa: F401
from openapi_server.models.get_contact import GetContact  # noqa: F401
from openapi_server.models.get_contacts import GetContacts  # noqa: F401
from openapi_server.models.update_contact_request import UpdateContactRequest  # noqa: F401


def test_get_contacts(client: TestClient):
    """Test case for get_contacts

    Получение всех контактов через пагинацию
    """
    params = [("page_token", 'page_token_example'),     ("page_size", 100)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/api/contacts",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_post_contact(client: TestClient):
    """Test case for post_contact

    Создание контакта
    """
    create_contact_request = {"number":"82223334455","city":"Moscow","name":"Alexander","description":"Лучший друг","age":11,"email":"Alexander22@mail.ru"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/api/contacts",
    #    headers=headers,
    #    json=create_contact_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_contact(client: TestClient):
    """Test case for get_contact

    Получение конкретного контакта
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/api/contact/{id}".format(id=33),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_put_contact(client: TestClient):
    """Test case for put_contact

    Полное изменение контакта
    """
    create_contact_request = {"number":"82223334455","city":"Moscow","name":"Alexander","description":"Лучший друг","age":11,"email":"Alexander22@mail.ru"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/api/contact/{id}".format(id=33),
    #    headers=headers,
    #    json=create_contact_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_patch_contact(client: TestClient):
    """Test case for patch_contact

    Изменение контакта
    """
    update_contact_request = {"number":"82223334455","city":"Moscow","name":"Alexander","description":"Лучший друг","age":11,"email":"Alexander22@mail.ru"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PATCH",
    #    "/api/contact/{id}".format(id=33),
    #    headers=headers,
    #    json=update_contact_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

