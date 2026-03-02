import pytest
import allure
from conftest import *
from config import *
from helpers import *

@allure.epic("Получение заказа")
@allure.tag('get order')
@pytest.mark.api_scooter
class TestApiGetOeder:

    @allure.title("Получение списка заказов")
    def test_api_get_orders_view_list_orders(self, api):
        '''Тест проверяет, что в тело ответа возвращается список заказов.'''
        with allure.step('Отправляем GET-запрос для получения списка заказов'):
            response = api.get(path = LIST_ORDER_URL)
            body = response.json()
        with allure.step('Проверяем статус код'):
            status_code = response.status_code
            assert status_code == 200, f'Неверный status code ответ. Ожидали: "200"; Получили: {status_code}; Ответ:"{body}'
        with allure.step('Проверяем тело ответа'):
            assert isinstance(body["orders"], list), (f"Ожидали список в поле 'orders', получили {type(body['orders'])}. Ответ: {body}")
