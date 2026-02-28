import pytest
import allure
from config import *
from selenium import webdriver 
from helpers import *
from api_client import ApiClient

@pytest.fixture
def api():
    """Фикстура для создания объекта класса ApiClient"""
    with allure.step('Открываем сессию api'):
        client = ApiClient()
    yield client
    client.close

@pytest.fixture
def registration_courier(api):
    """Фикстура для регистрации пользователя"""
    yield register_new_courier_and_return_login_password(api)
