import allure
import requests
from requests import Response, Session
import json
from config import *

class ApiClient:
    
    def __init__(self,*, headers:dict = {"Accept": "application/json","Content-Type": "application/json",}, verify: bool = True):
        self.base_url = BASE_URL.rstrip("/")
        self.verify = verify
        self.session: Session = requests.Session()
        self.session.headers = headers
    
    def url(self, path: str) -> str:
        """Метод формирования полного url"""
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path: str, **kwargs):
        """Метод для GET-запроса"""
        with allure.step(f"Отправляем GET-запрос на '{path}'"):
            return self.session.get(self.url(path), **kwargs)

    def post(self, path: str, **kwargs):
        """Метод для POST-запроса"""
        with allure.step(f"Отправляем POST-запрос на '{path}'"):
            return self.session.post(self.url(path), **kwargs)

    def put(self, path: str, **kwargs):
        """Метод для PUT-запроса"""
        with allure.step(f"Отправляем PUT-запрос на '{path}'"):
            return self.session.put(self.url(path), **kwargs)
        
    def delete(self, path: str, **kwargs):
        """Метод для DELETE-запроса"""
        with allure.step(f"Отправляем DELETE-запрос на '{path}'"):
            return self.session.delete(self.url(path), **kwargs)

    def close(self):
        self.session.close()