# -*- coding: utf-8 -*-
import requests, hashlib
from defusedxml.ElementTree import parse
from io import StringIO

DEFAULT_TIMEOUT = 4

class IikoBiz:

    def __init__(self, ip=None, port=None, login=None, password=None, token=None, timeout=DEFAULT_TIMEOUT):
        self._address = 'http://' + ip + ':'+ (str(port) or '80') + '/'
        self._login = login
        self._password = password
        self._token = token
        self.set_timeout(timeout)

    @property
    def timeout(self):
        return self._timeout

    def set_timeout(self, timeout=DEFAULT_TIMEOUT):
        self._timeout = timeout

    @property
    def token(self):
        return str(self._token)

    def login(self):
        try:
            url = self._address + 'api/0/auth/access_token?user_id=' + self._login + '&user_secret=' + self._password 
            login = requests.get(url, timeout=self.timeout)
            if login.status_code == 200:
                self._token = login.text
            return login

        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить токен " + "\n" + self.login)

    def get(self, path, params=None):
        """
        Возвращает request по заданному пути с использованием токена авторизации
        """
        try:
            url = self._address + path + "?key=" + self.token
            return requests.get(url=url, params=params, timeout=self.timeout)
        except Exception as e:
            print(path)
            print(e)

    def post(self, path, data=None, json=None, headers=None):
        """
        Возвращает request по заданному пути с использованием токена авторизации
        """
        try:
            url = self._address + path + "?key=" + self.token
            return requests.post(url=url, data=data, json=json, headers=headers, timeout=self.timeout)
        except Exception as e:
            print(path)
            print(e)





    def organization(self, token):

        try:

            return requests.get(
                'https://iiko.biz:9900/api/0/organization/list?access_token=' +
                token).json()

        except requests.exceptions.ConnectTimeout:
            print(
                "Не удалось получить список организаций " + "\n" + self.login)

    def courier(self, token, org):

        try:
            return requests.get(
                'https://iiko.biz:9900/api/0/rmsSettings/getCouriers?access_token='
                + token + '&organization=' + org).json()

        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить курьеров " + "\n" + self.login)

    def orders_courier(self, token, org, courier):

        try:
            return requests.get(
                'https://iiko.biz:9900/api/0/orders/get_courier_orders?access_token='
                + token + '&organization=' + org + '&courier=' + courier +
                '&request_timeout=00%3A02%3A00').json()

        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить заказы " + "\n" + self.login)

    """Все заказы"""

    def all_orders(self, token, **kwargs):

        try:
            return requests.get(
                'https://iiko.biz:9900/api/0/orders/deliveryOrders?access_token='
                + token,
                params=kwargs).json()

        except requests.exceptions.ConnectTimeout:
            print("Не получить заказы " + "\n" + self.login)

    """История заказа гостя"""

    def customer_history(self, token, org, customer):

        try:
            return requests.get(
                'https://iiko.biz:9900/api/0/orders/deliveryHistoryByCustomerId?access_token='
                + token + '&organization=' + org + '&customerId=' + customer +
                '&request_timeout=00%3A02%3A00').json()

        except requests.exceptions.ConnectTimeout:
            print("Не получить заказы " + "\n" + self.login)

    def nomenclature(self, token, org):
        """Получить дерево номенклатуры"""
        try:
            return requests.get('https://iiko.biz:9900/api/0/nomenclature/' +
                                org + '?access_token=' + token).json()

        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить номенклатуру " + "\n" + self.login)

    "-------------------Города, улицы, регионы-------------------"

    def cities(self, token, org):
        """Список городов"""
        try:
            return requests.get(
                'https://iiko.biz:9900/api/0/cities/cities?access_token=' +
                token + '&organization=' + org).json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить список городов" + "\n" + self.login)

    def cities_list(self, token, org):
        """возвращает список всех городов заданной организации"""
        try:
            return requests.get(
                'https://iiko.biz:9900/api/0/citiesList/cities?access_token=' +
                token + '&organization=' + org).json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить список городов" + "\n" + self.login)

    def streets(self, token, org, citi_id):
        """возвращает список улиц города заданной организации"""
        try:
            return requests.get(
                'https://iiko.biz:9900/api/0/citiesList/streets?access_token='
                + token + '&organization=' + org + '&city=' + citi_id).json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить список улиц" + "\n" + self.login)

    "--------------------------------------Стоп-листы--------------------------------------"

    def stop_list(self, token, org):
        """Получить стоп-лист по сети ресторанов"""
        try:
            return requests.get(
                'https://iiko.biz:9900/api/0/stopLists/getDeliveryStopList?access_token='
                + token + '&organization=' + org).json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить список улиц" + "\n" + self.login)

    "--------------------------------------Журнал событий--------------------------------------"

    def events(self, token, timeout=None):
        """Получить стоп-лист по сети ресторанов"""
        try:
            return requests.get(
                'https://iiko.biz:9900/api/0/events/events?access_token=' +
                token + '&request_timeout=' + timeout).json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить список улиц" + "\n" + self.login)

    def events_meta(self, token, body, timeout=None):
        """Получить мета информацию журнала событий (описание возвращаемых данных)"""
        try:
            return requests.post(
                'https://iiko.biz:9900/api/0/events/eventsMetadata?access_token='
                + token + '&request_timeout=' + timeout,
                body=body).json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить список улиц" + "\n" + self.login)

    def events_session(self, token, body, timeout=None):
        """Получить информацию о кассовых сменах"""
        try:
            return requests.post(
                'https://iiko.biz:9900/api/0/events/sessions?access_token=' +
                token + '&request_timeout=' + timeout,
                body=body).json()
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить список улиц" + "\n" + self.login)