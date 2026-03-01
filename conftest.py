import pytest
import allure
from config import *
from helpers import *
from api_client import ApiClient

@pytest.fixture
def api():
    """Фикстура для создания объекта класса ApiClient"""
    with allure.step('Открываем сессию api'):
        client = ApiClient()
    yield client
    with allure.step('Закрываем сессию api'):
        client.close

@pytest.fixture
def registration_courier(api):
    """Фикстура для регистрации курьерая и удаления курьера после теста"""
    courier = register_new_courier_and_return_login_password(api)
    yield courier
    id = get_id_courier(api, courier[0], courier[1])
    delete_courier_by_id(api, id)

@pytest.fixture
def delete_courier(api):
    """Фикстура для удаления курьера после теста"""
    courier_data = {}
    yield courier_data
    login = courier_data.get("login")
    password = courier_data.get("password")
    if login and password:
        id = get_id_courier(api, login, password)
        delete_courier_by_id(api, id)

@pytest.fixture
def delete_order(api):
    """Фикстура для удаления заказа после теста"""
    track_order = {}
    yield track_order
    if track_order:
        cancel_order(api, track_order["track"])