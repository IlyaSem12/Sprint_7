# Финальный проект 7 спринта

## Описание
Проект содержит UI-автотесты для веб-приложения для 7 спринта яндекс практикума.

Тестирование реализовано на Python с использованием:
- pytest
- requests
- allure-report
---

## Структура проекта


SPRINT_7
```
SPRINT_7
│
├── tests/
│ ├── test_api_create_courier.py
│ ├── test_api_login_courier.py
│ ├── test_api_create_order.py
│ ├── test_api_get_order.py
│
├── api_client.py
├── config.py
├── helpers.py
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```
---

## Покрываемый функционал

### Курьеры
- Создание курьера
- Проверка невозможности создания дубликата
- Авторизация курьера

### Заказы
- Создание заказа
- Получение списка заказов
- Проверка типа ответа (`orders` — список)

---

## Установка и запуск

### Клонировать репозиторий

```bash
git clone <git@github.com:IlyaSem12/Sprint_7.git>
cd SPRINT_7
```