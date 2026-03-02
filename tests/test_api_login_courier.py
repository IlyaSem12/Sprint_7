import pytest
import allure
from conftest import *
from config import *
from helpers import *

@allure.epic("Логин курьера")
@allure.tag('login courier')
@pytest.mark.api_scooter
class TestApiLoginCourier:

    @allure.title("Проверка успешной авторизации курьера")
    def test_api_success_login_courier_view_id_and_status_code_200(self,api, registration_courier):
        '''Тест проеряет успешную авторизацю курьера, запрос возвращает ошибку {id: 12345}'''
        payload = {
            "login": registration_courier[0],
            "password": registration_courier[1],
        }
        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        with allure.step('Отправляем POST-запрос для авторизации курьера'):
            response = api.post(path = LOGIN_COURIER_URL, json = payload)
            body = response.json()
        with allure.step('Проверяем статус код'):
            status_code = response.status_code
            assert status_code == 200, f'Неверный status code ответ. Ожидали: "200"; Получили: {status_code}; Ответ:"{body}"'
        with allure.step('Проверяем тело ответа'):
            assert "id" in body and body["id"], (f'Вход не был произведен. Ответ: {body}')

    @allure.title("Проверка на присутвие обязательных полей при регистрации")
    @pytest.mark.parametrize('payload, message',[
        pytest.param( {"login": 'ninja_111111111'},'Отсутствует поле "password"', id='missing_field_password'),
        pytest.param( {"password": '123123123'},'Отсутствует поле "login"', id='missing_field_login'),
    ])
    def test_api_fail_login_courier_should_return_error_when_field_is_missing(self, api, payload, message):
        '''Тест проеряет, что если одного из обязательных полей нет при авторизации курьера, запрос возвращает ошибку {"message": "message": "Недостаточно данных для входа"}'''
        allure.dynamic.title(f"Пороверка на обязательные поля:{message}")
        with allure.step('Отправляем POST-запрос для авторизации курьера'):
            response = api.post(path = LOGIN_COURIER_URL, json = payload)
            body = response.json()
        with allure.step('Проверяем статус код'):
            status_code = response.status_code
            assert status_code == 400, f'Неверный status code ответ. Ожидали: "400"; Получили: {status_code}; Ответ:"{body}"'
        with allure.step('Проверяем тело ответа'):
            assert body.get("message") == ERROR_LOGIN_MISSING_FIELD, (f'Был авторизован курьер без ключевого поля. Ответ:"{body}"')
    
    @pytest.mark.parametrize('wrong_value, wrong_field, message',[
        pytest.param('ninja_111111111','login','Неверный login', id='wrong_login'),
        pytest.param('123123123','password','Неверный password"', id='wrong_password'),
    ])
    def test_api_fail_login_courier_with_incorrect_credentials_returns_error(self,api,registration_courier,wrong_value, wrong_field, message):
        '''Тест проеряет что, запрос возвращает ошибку {"message": "message": "Учетная запись не найдена"}, если неправильно указать логин или пароль'''
        allure.dynamic.title(f"Логин с некорректными данными:{message}")
        payload = {
            "login": registration_courier[0],
            "password": registration_courier[1],
        }
        payload[wrong_field] = wrong_value
        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        with allure.step('Отправляем POST-запрос для авторизации курьера'):
            response = api.post(path = LOGIN_COURIER_URL, json = payload)
            body = response.json()
        with allure.step('Проверяем статус код'):
            status_code = response.status_code
            assert status_code == 404, f'Неверный status code ответ. Ожидали: "404"; Получили: {status_code}; Ответ:"{body}"'
        with allure.step('Проверяем тело ответа'):
            assert body.get("message") == ERROR_LOGIN, (f'Ожидали "{ERROR_LOGIN}", получили: {body}')
    