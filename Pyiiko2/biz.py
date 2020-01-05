# -*- coding: utf-8 -*-
import requests, hashlib
from defusedxml.ElementTree import parse
from io import StringIO

DEFAULT_TIMEOUT = 4

class IikoBiz:

    def __init__(self, ip=None, port=None, login=None, password=None, token=None, timeout=DEFAULT_TIMEOUT):
        self._ip = ip
        self._port = port
        self._login = login
        self._password = password
        self._token = token
        self.set_timeout(timeout)

    @property
    def address(self):
        return 'http://' + self._ip + ':'+ (str(self._port) or '80') + '/'

    def set_address(ip=None, port=None):
        self._ip = ip or self._ip
        self._port = port or self._port

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
            url = self.address + 'api/0/auth/access_token?user_id=' + self._login + '&user_secret=' + self._password 
            login = requests.get(url, timeout=self.timeout)
            if login.status_code == 200 and len(login.text)>2:
                self._token = login.text[1:-1]
            return login

        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить токен " + "\n" + self.login)

    def get(self, path, params=None):
        """
        Возвращает request по заданному пути с использованием токена авторизации
        """
        try:
            url = self.address + path + "?access_token=" + self.token
            return requests.get(url=url, params=params, timeout=self.timeout)
        except Exception as e:
            print(path)
            print(e)

    def post(self, path, data=None, json=None, headers=None):
        """
        Возвращает request по заданному пути с использованием токена авторизации
        """
        try:
            url = self.address + path + "?access_token=" + self.token
            return requests.post(url=url, data=data, json=json, headers=headers, timeout=self.timeout)
        except Exception as e:
            print(path)
            print(e)


    def organization(self, **kwargs):
        return self.get("api/0/organization/list", params=kwargs)

    def courier(self, **kwargs):
        return self.get("api/0/rmsSettings/getCouriers", params=kwargs)

    def orders_courier(self, **kwargs):
        return self.get("api/0/orders/get_courier_orders", params=kwargs)

    def all_orders(self, **kwargs):
        return self.get("api/0/orders/deliveryOrders", params=kwargs)

    def customer_history(self, **kwargs):
        return self.get("api/0/orders/deliveryHistoryByCustomerId", params=kwargs)

    def nomenclature(self, **kwargs):
        return self.get("api/0/nomenclature", params=kwargs)

    def cities(self, **kwargs):
        return self.get("api/0/cities/cities", params=kwargs)

    def cities_list(self, **kwargs):
        return self.get("api/0/citiesList/cities", params=kwargs)

    def streets(self, **kwargs):
        return self.get("api/0/citiesList/streets", params=kwargs)

    def stop_list(self, **kwargs):
        return self.get("api/0/stopLists/getDeliveryStopList", params=kwargs)

    def events(self, **kwargs):
        return self.get("api/0/events/events", params=kwargs)

    def events_meta(self, **kwargs):
        return self.get("api/0/events/eventsMetadata", params=kwargs)

    def events_session(self, **kwargs):
        return self.get("api/0/events/sessions", params=kwargs)
