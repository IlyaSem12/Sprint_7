import pytest
import allure
from conftest import *
from config import *
from helpers import *

@allure.epic("Создание курьера")
@allure.tag('create courier')
@pytest.mark.api_scooter
class TestApiCreateCourier:
    
    @pytest.mark.parametrize('password, firstName, message',[
        pytest.param("Pass1234", "Naruto",'Успешная регистрация', id='defolt_registration'),
        pytest.param( "123456", "a"*30,'Длинное имя', id='long_firstname'),
        pytest.param( "1", "Geralt",'Короткий пароль', id='short_password'),
        pytest.param( "Pass1234",'Пробелы в имени', "Geralt of Rivia", id='space_in_name'),
    ],)
    def test_api_success_create_courier_view_response_true_and_status_code_201(self, api,delete_courier, password, firstName, message):
        '''Тест проеряет регистрацию курьера через api, запрос возвращает {ok: true} при успешной регистрации'''
        allure.dynamic.title(f"Успешная регистрация курьера:{message}")
        login = generate_login()# генерируем уникальный лонгин
        payload = {
            "login": login,
            "password": password,
            "firstName": firstName
        }# собираем тело запроса
        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        with allure.step('Отправляем POST запрос для регистрации курьера'):
            response = api.post(path = COURIER_URL, json = payload)
        with allure.step('Проверяем статус код'):
            status_code = response.status_code
            assert status_code == 201, f'Неверный status code ответ. Ожидали: "201"; Получили: {status_code}'
        with allure.step('Проверяем тело ответа'):
            body = response.json()
            assert body.get("ok") is True, (f'Курьер не был создан. Ответ: {body}')
        delete_courier["login"] = login
        delete_courier["password"] = password

    @allure.title("Проверка уникальности курьера при регистрации")
    def test_api_fail_create_identical_courier_view_error_response_and_status_code_409(self, api, registration_courier):
        '''Тест проеряет, что нельзя создать двух одинаковых курьеров через api и возвращает {"message": "Этот логин уже используется"}'''
        payload = {
            "login": registration_courier[0],
            "password": registration_courier[1],
            "firstName": registration_courier[2],
        }
        with allure.step('Отправляем POST запрос для регистрации курьера'):
            response = api.post(path = COURIER_URL, json = payload)
        with allure.step('Проверяем статус код'):
            status_code = response.status_code
            assert status_code == 409, f'Неверный status code ответ. Ожидали: "409"; Получили: {response.json()}'
        with allure.step('Проверяем тело ответа'):
            body = response.json()
            assert body.get("message") == ERROR_REGISTRATION_INDENTICAL_COURIER, (f'Был создан дубликат курьера')
    
    @pytest.mark.parametrize('payload, message',[
        pytest.param( {"login": 'test_user',"firstName": 'Naruto'},'Отсутствует поле "password"', id='missing_field_password'),
        pytest.param( {"password": '123123123',"firstName": 'Naruto'},'Отсутствует поле "login"', id='missing_field_login'),
    ],)
    def test_api_fail_create_courier_should_return_error_when_field_is_missing(self, api, payload, message):
        '''Тест проеряет, что если одного из обязательных полей нет при регистрации курьера, запрос возвращает ошибку {"message": "message": "Недостаточно данных для создания учетной записи"}'''
        allure.dynamic.title(f"Проверка на обязательные поля:{message}")
        with allure.step('Отправляем POST запрос для регистрации курьера'):
            response = api.post(path = COURIER_URL, json = payload)
        with allure.step('Проверяем статус код'):
            status_code = response.status_code
            assert status_code == 400, f'Неверный status code ответ. Ожидали: "400"; Получили: {status_code}'
        with allure.step('Проверяем тело ответа'):
            body = response.json()
            assert body.get("message") == ERROR_REGISTRATION_MISSING_FIELD, (f'Был создан курьер без ключевого поля')
    