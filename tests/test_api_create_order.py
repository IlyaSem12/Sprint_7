import pytest
import allure
from conftest import *
from config import *
from helpers import *

@allure.epic("Создание заказа")
@allure.tag('create order')
@pytest.mark.api_scooter
class TestApiCreateOeder:

    @pytest.mark.parametrize('color, message',[
        pytest.param(["BLACK"],'Черный цвет', id='black_color'),
        pytest.param(["GREY"],'Серый цвет', id='gray_color'),
        pytest.param(["BLACK","GREY"],'Оба цвета', id='black_color'),
        pytest.param( None,'Цвета не указаны', id='none_color'),
    ])
    def test_api_success_create_order_with_various_color_combinations_return_track(self, api, delete_order, color,message):
        allure.dynamic.title(f"Создание заказа:{message}")
        payload = DATA_ORDER
        if color is not None:
            payload["color"] = color
        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        with allure.step('Отправляем POST-запрос для создания заказа на самокат'):
            response = api.post(path = LIST_ORDER_URL, json = payload)
            body = response.json()
        with allure.step('Проверяем статус код'):
            status_code = response.status_code
            assert status_code == 201, f'Неверный status code ответ. Ожидали: "201"; Получили: {status_code}; Ответ:"{body}"'
        with allure.step('Проверяем тело ответа'):
            assert 'track' in body and body["track"], (f'Поле "track" не найдено или пустое. Ответ: {body}')
        delete_order["track"] = body["track"]