# -*- coding: utf-8 -*-
import requests
from defusedxml import etree
from io import StringIO

DEFAULT_TIMEOUT = 4


class IikoServer(object):
    """Класс отвечающий за работы с iikoSeverApi


    """

    def __init__(self, ip=None, port=None, login=None, passhash=None, token=None, timeout=DEFAULT_TIMEOUT):
        self.address = 'http://' + ip + ':'+ (str(port) or '80') + '/resto/'
        self._login = login
        self._passhash = passhash
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


    def __del__(self):
        if self._token is not None:
            self.logout()

    def login(self):
        """Метод получает новый токен
        .. note::

            при авторизации вы занимаете один слот лицензии. Token,
            который вы получаете при авторизации, можно использовать до того момента,
             пока он не протухнет ( не перестанет работать). И если у вас только одна
             лицензия сервера, а вы уже получили token, следующее обращение к серверу за
             token-ом вызовет ошибку. Если вам негде хранить token при работе с сервером API,
             рекомендуем вам разлогиниться, что приводит к отпусканию лицензии.

            """

        try:
            # Уничтожаем токен, если он он существует
            if self._token is not None:
                self.logout()

            url = self.address + 'api/auth?login=' + self._login + "&pass=" + self._passhash
            login = requests.get(url=url, timeout=self.timeout)
            if login.status_code == 200:
                self._token = login.text
            return login

        except Exception as e:
            print(e)

    def logout(self):
        """Уничтожение токена

        """

        try:
            logout = requests.get(
                self.address + 'api/logout?key=' + self.token)
            print("\nТокен уничтожен: " + self.token)
            self._token = None
            return logout

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    def version(self):
        """Позволяет узнать версию iiko

        :returns: Версия iiko в формате string
        """
        try:
            ver = requests.get(
                self.address + 'get_server_info.jsp?encoding=UTF-8').text
            tree = etree.parse(StringIO(ver))
            version = ''.join(tree.xpath(r'//version/text()'))
            return version

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    def server_info(self):
        """Вовращает json файл с информацией о сервере и статусе лицензии

                :returns: request
                """
        try:
            return requests.get(
                self.address + 'get_server_info.jsp?encoding=UTF-8')

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

# ----------------------------------Корпорации----------------------------------

    def departments(self):
        """Иерархия подразделений

        .. csv-table:: Типы подразделений
           :header: "Код", "Наименование"
           :widths: 15, 20

           "CORPORATION", Корпорация
           "JURPERSON", Юридическое лицо
           ORGDEVELOPMENT, Структурное подразделение
           DEPARTMENT, Торговое предприятие
           MANUFACTURE, Производство
           CENTRALSTORE, Центральный склад
           CENTRALOFFICE, Центральный офис
           SALEPOINT, Точка продаж
           STORE, Склад

            :returns: request

        """
        try:
            urls = self.address + "api/corporation/departments?key=" + self.token
            return requests.get(url=urls, timeout=self.timeout)
        except Exception as e:
            print(e)

    def stores(self):
        """Список складов

        :returns: request


        """
        try:
            ur = self.address + 'api/corporation/stores?key=' + self.token
            return requests.get(ur, timeout=self.timeout)
        except Exception as e:
            print(e)

    def groups(self):
        """Список групп и отделений

        :returns: request

        """
        try:
            ur = self.address + 'api/corporation/groups?key=' + self._token
            return requests.get(ur, timeout=self.timeout)

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    def terminals(self):
        """Список терминалов.

            :returns: request

        """
        try:
            ur = self.address + 'api/corporation/terminals?key=' + self.token
            return requests.get(ur, timeout=self.timeout)

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    def departments_find(self, code):
        """Поиск подразделения.

        :param name: (optional) Код торгового предприятия. Значение элемента <code> из структуры corporateItemDto \
                                    Регулярное выражение. Если задать просто строку, то ищет любое вхождение этой строки в код ТП с учетом регистра


        :type code: [departmentCode]

        :returns: request

        """
        try:
            ur = self.address + 'api/corporation/departments/search?key=' + self.token
            return requests.get(
                ur, params=code, timeout=self.timeout)

        except Exception as e:
            print(e)

    def stores_find(self, code):
        """Список складов.


        :param code: Код склада - регулярное выражение. Если задать просто строку, то ищет любое вхождение \
                        этой строки в код склада с учетом регистра.
        :type code: [storeCode]

        :returns: request

        """
        try:
            url = self.address + 'api/corporation/stores/search?key=' + self.token
            return requests.get(url, params=code)

        except requests.exceptions.ConnectTimeout:
            print("Не удалось подключиться к серверу")

    def groups_search(self, **kwargs):
        """Поиск групп отделений.


        :param name: Название группы.
        :type name: regex
        :param departmentId: ID подразделения
        :type departmentId: string
        :returns: request
        """
        try:
            urls = self.address + 'api/corporation/terminal/search?key=' + self.token
            return requests.get(
                url=urls, params=kwargs, timeout=self.timeout)

        except Exception as e:
            print(e)

    def terminals_search(self, anonymous=False, **kwargs):
        """Поиск терминала.


        :param anonymous: (bool) Фронты имеют anonymous=false, бекофисы и системные терминалы — true.
        :param name: (regex) - (optional) Имя терминала в том виде, как он отображается в бекофисе.
        :param computerName: (regex) - (optional) Имя компьютера

        :returns: request
        """
        try:
            urls = self.address + 'api/corporation/terminal/search?key=' + self.token + '&anonymous=' + anonymous
            return requests.get(
                urls, params=kwargs, timeout=self.timeout)

        except Exception as e:
            print(e)

# ----------------------------------Работники----------------------------------
    def employees(self):
        """
        Работники
        :returns: request
        """
        try:
            urls = self.address + 'api/employees?key=' + self.token
            return requests.get(urls, timeout=self.timeout)

        except Exception as e:
            print(e)

# ----------------------------------События----------------------------------
    def events(self, **kwargs):
        """Список событий.


        :param from_time: (yyyy-MM-ddTHH:mm:ss.SSS) - (optional) Время с которого запрашиваются события, \
        в формате ISO: yyyy-MM-ddTHH:mm:ss.SSS, по-умолчанию – начало текущих суток.
        :param to_time: (yyyy-MM-ddTHH:mm:ss.SSS) - (optional) Время по которое (не включительно) запрашиваются \
        события в формате ISO: yyyy-MM-ddTHH:mm:ss.SSS,, по-умолчанию граница не установлена.
        :param from_rev: (int) - (optional) Ревизия, с которой запрашиваются события, число. Каждый ответ \
        содержит тэг revision, значение которого соответствует ревизии, по которую включительно отданы события; \
        при новых запросах следует использовать revision + 1 (revision из предыдущего ответа) для получения только \
        новых событий. В штатном режиме одно и тоже событие повторно с разными ревизиями не приходит, однако \
        такой гарантии не даётся. ID (UUID) события уникален, может использоваться в качестве ключа.

        :returns: request
        """
        try:
            ur = self.address + 'api/events?key=' + self.token
            return requests.get(
                ur, params=kwargs, timeout=self.timeout)

        except Exception as e:
            print(e)

    def events_filter(self, body):
        """
        Список событий по фильтру событий и номеру заказа.


        :param body: Список id событий, по которым производится фильтрация (application/xml).

        Пример body

        .. code-block:: xml

            <eventsRequestData>
                <events>
                    <event>orderCancelPrecheque</event>
                    <event>orderPaid</event>
                </events>
                <orderNums>
                    <orderNum>175658</orderNum>
                </orderNums>
            </eventsRequestData>

        :returns: request
        """

        try:
            ur = self.address + 'api/events?key=' + self.token
            return requests.post(
                ur, data=body, timeout=self.timeout)

        except Exception as e:
            print(e)

    def events_meta(self):
        """
        Дерево событий.

        :returns: request

        """
        try:
            urls = self.address + 'api/events/metadata?key=' + self.token
            return requests.get(urls, timeout=self.timeout)

        except Exception as e:
            print(e)

# ----------------------------------Продукты----------------------------------

    def products(self, includeDeleted=True):
        """Номенклатура.

        .. csv-table:: Тип элемента номенклатуры
           :header: "Код", "Наименование"
           :widths: 15, 20

           "GOODS", "Товар"
           "DISH", Блюдо
           PREPARED, Заготовка
           SERVICE, Услуга
           MODIFIER, Модификатор
           OUTER, Внешние товары
           PETROL, Топливо
           RATE, Тариф

        .. csv-table:: Типы групп продукта
           :header: "Код", "Наименование", Комментарий
           :widths: 15, 20, 20

           "PRODUCTS", "Продукт",
           "MODIFIERS", Модификатор, "Используется только в номенклатуре, которая загружается /
           и выгружается в/из RKeeper/StoreHouse"


        :param includeDeleted: (bool) - (optional) Включать ли удаленные элементы номенклатуры в результат. По умолчанию false. Реализовано в 5.0 и новее.

        :returns: request
        """
        try:
            urls = self.address + 'api/products?key=' + self.token
            return requests.get(
                urls, params=includeDeleted, timeout=self.timeout)

        except Exception as e:
            print(e)

    def products_find(self, **kwargs):
        """Поиск номенклатуры

        :param includeDeleted: (bool) Включать ли удаленные элементы номенклатуры в результат. По умолчанию false. Реализовано в 5.0 и новее.
        :param name: (regex) - (optional) Название.
        :param code: (regex) - (optional) Код быстрого набора в IikoFront.
        :param mainUnit: (regex) - (optional) Базовая единица измерения.
        :param num: (regex) - (optional) Артикул.
        :param cookingPlaceType: (regex) - (optional) Тип места приготовления.
        :param productGroupType: (regex) - (optional) Тип родительской группы.
        :param productType: (regex) - (optional) Тип номенклатуры.

        Выгрузка и поиск идет по всем неудаленным элементам номенклатуры. Включая товары поставщика. Т.к. сейчас \
        нет возможности удалить товар поставщика, то выгрузка потянет все товары поставщика, даже те, которые реально не используются и не участвуют ни в одной связке товар у нас - товар поставщика.
        :returns: request

        """
        try:
            urls = self.address + 'api/products/search/?key=' + self.token
            return requests.get(
                urls, params=kwargs, timeout=self.timeout)

        except Exception as e:
            print(e)

# ----------------------------------Поставщики----------------------------------

    def suppliers(self):
        """Список всех поставщиков

        :returns: request
        """
        try:
            urls = self.address + 'api/suppliers?key=' + self.token
            return requests.get(urls, timeout=self.timeout)

        except Exception as e:
            print(e)

    def suppliers_find(self, name='', code=''):
        """Поиск поставщика

        :param name: (regex) - (optional) регулярное выражение имени поставщика.
        :param code: (regex) - (optional) регулярное выражение кода поставщика.

        :returns: request
        """
        try:
            urls = self.address + 'api/suppliers?key=' + self.token
            payload = {'name': name, 'code': code}
            return requests.get(
                urls, params=payload, timeout=self.timeout)

        except Exception as e:
            print(e)

    def suppliers_price(self, code, date=None):
        """Поиск поставщика

        :param code: (date - DD.MM.YYYY) - (optional) Дата начала действия прайс-листаДата начала действия \
        прайс-листа, необязательный. Если параметр не указан, возвращается последний прайс-лист.
        :returns: request
        """
        try:
            urls = self.address + 'api/suppliers/' + code + '/pricelist?key=' + self.token
            return requests.get(
                urls, params=date, timeout=self.timeout)

        except Exception as e:
            print(e)

# ----------------------------------Отчеты----------------------------------

    def olap(self, report=None, data_from=None, data_to=None, **kwargs):
        """OLAP-отчет

        :param report: (Тип отчета)
            | ``SALES`` - По продажам.
            | ``TRANSACTIONS`` - По транзакциям.
            | ``DELIVERIES`` - По доставкам.
            | ``STOCK`` - Контролю хранения.
        :param groupRow: (Поля группировки) например:
            ``groupRow=WaiterName&groupRow=OpenTime.``

            Для определения списка доступных полей см.
                - Описание полей OLAP отчета по продажам.
                - Описание полей OLAP отчета по проводкам.
                - Описание полей OLAP отчета по доставкам.
            По полю можно проводить группировку, если значение в колонке Grouping для поля равно true.

        :param groupCol: Поля для выделения значений по колонкам.

            Для определения списка доступных полей см.
                - Описание полей OLAP отчета по продажам.
                - Описание полей OLAP отчета по проводкам.
                - Описание полей OLAP отчета по доставкам.
            По полю можно проводить группировку, если значение в колонке Grouping для поля равно true.

        :param agr: Поля агрегации, например: agr=DishDiscountSum&agr=VoucherNum

            Для определения списка доступных полей см.
                - Описание полей OLAP отчета по продажам.
                - Описание полей OLAP отчета по проводкам.
                - Описание полей OLAP отчета по доставкам.
            По полю можно проводить группировку, если значение в колонке Grouping для поля равно true.

        :returns: request

        """
        try:
            urls = self.address + 'api/reports/olap?report=' + report + '&key=' + self.token + '&from=' + data_from + '&to=' + data_to
            return requests.get(
                urls, params=kwargs, timeout=self.timeout)

        except Exception as e:
            print(e)

    def store_operation(self,
                        stores=None,
                        documentTypes=None,
                        productDetalization=True,
                        showCostCorrections=True,
                        presetId=None):
        """Отчет по складским операциям

        :param dateFrom: (DD.MM.YYYY) Начальная дата.
        :param dateTo: (DD.MM.YYYY) Конечная дата.
        :param stores: (GUID) - (optional) Список складов, по которым строится отчет. Если null или empty, строится по всем складам.
        :param documentTypes: () - (optional) Типы документов, которые следует включать. Если null или пуст, включаются все документы.
        :param productDetalization: (boolean) - (по умолчанию true) Если истина, отчет включает информацию по товарам, но не включает дату. \
        Если ложь - отчет включает каждый документ одной строкой и заполняет суммы документов.
        :param showCostCorrections: (boolean) - Включать ли коррекции себестоимости. Данная опция учитывается только если задан фильтр \
        по типам документов. В противном случае коррекции включаются.
        :param presetId: (GUID) - (optional) Id преднастроенного отчета. Если указан, то все настройки, кроме дат, игнорируются.

        :returns: request

        """
        try:
            urls = self.address + 'api/reports/storeOperations?key=' + self.token
            return requests.get(
                urls,
                params={
                    stores, documentTypes, productDetalization,
                    showCostCorrections, presetId
                },
                timeout=self.timeout)

        except Exception as e:
            print(e)

    def store_presets(self):
        """Пресеты отчетов по складским операциям

        :returns: request

        """
        try:
            urls = self.address + 'api/reports/storeReportPresets?key=' + self.token
            return requests.get(urls, timeout=self.timeout)

        except Exception as e:
            print(e)

    def product_expense(self, departament, **kwargs):
        """Расход продуктов по продажам

        :param department: (GUID) Подразделение
        :param dateFrom: (DD.MM.YYYY) Начальная дата.
        :param dateTo: (DD.MM.YYYY) Конечная дата.
        :param hourFrom: (hh) Час начала интервала выборки в сутках (по умолчанию -1, все время), по умолчанию -1.
        :param hourTo: (hh) Час окончания интервала выборки в сутках (по умолчанию -1, все время), по умолчанию -1.

        :returns: request
        """
        try:
            urls = self.address + 'api/reports/productExpense?key=' + self.token
            return requests.get(
                urls, params={departament, kwargs},
                timeout=self.timeout)

        except Exception as e:
            print(e)

    def sales(self, departament, dishDetails=False, allRevenue=True, **kwargs):
        """Отчет по выручке

        :param department: (GUID) Подразделение
        :param dateFrom: (DD.MM.YYYY) Начальная дата.
        :param dateTo: (DD.MM.YYYY) Конечная дата.
        :param hourFrom: (hh) Час начала интервала выборки в сутках (по умолчанию -1, все время), по умолчанию -1.
        :param hourTo: (hh) Час окончания интервала выборки в сутках (по умолчанию -1, все время), по умолчанию -1.
        :param dishDetails: (boolean) Включать ли разбивку по блюдам (true/false), по умолчанию false.
        :param allRevenue: (boolean)  Фильтрация по типам оплат (true - все типы, false - только выручка), по умолчанию true.

        :returns: request
        """

        try:
            urls = self.address + 'api/reports/sales?key=' + self.token + \
                   '&department=' + departament
            return requests.get(
                urls,
                params={dishDetails, allRevenue, kwargs},
                timeout=self.timeout)

        except Exception as e:
            print(e)

    def mounthly_plan(self, departament, **kwargs):
        """План по выручке за день

        :param department: (GUID) Подразделение
        :param dateFrom: (DD.MM.YYYY) Начальная дата.
        :param dateTo: (DD.MM.YYYY) Конечная дата.

        :returns: request


        """
        try:
            urls = self.address + 'api/reports/monthlyIncomePlan?key=' + self.token + \
                   '&department=' + departament
            return requests.get(
                urls, params=kwargs, timeout=self.timeout)

        except Exception as e:
            print(e)

    def ingredient_entry(self, departament, includeSubtree=False, **kwargs):
        """Отчет о вхождении товара в блюдо

        :param department: (GUID) Подразделение
        :param dateFrom: (DD.MM.YYYY) Начальная дата.
        :param dateTo: (DD.MM.YYYY) Конечная дата.
        :param productArticle: (string) Артикул продукта (приоритет поиска:productArticle, product)
        :param includeSubtree: (bool) - (optional) Включать ли в отчет строки поддеревьев (по умолчанию false)

        :returns: request
        """
        try:
            urls = self.address + 'api/reports/ingredientEntry?key=' + self.token
            return requests.get(
                urls,
                params={departament, includeSubtree, kwargs},
                timeout=self.timeout)

        except Exception as e:
            print(e)

    def olap2(self,
              json=None):
        """Поля OLAP-отчета

        :param json: (optional) Json с полями
        
        :return: response

        """
        try:
            url = self.address + 'api/v2/reports/olap?key=' + self.token
            return requests.post(url,json=json,timeout=self.timeout)

        except Exception as e:
            print(e)

    def olap2columns(self, reportType):
        """Поля OLAP-отчета

        :param reportType: (Тип отчета)
            | ``SALES`` - По продажам.
            | ``TRANSACTIONS`` - По транзакциям.
            | ``DELIVERIES`` - По доставкам.
        
        :return: response

        """
        try:
            url = self.address + 'api/v2/reports/olap/columns?key=' + self.token
            return requests.get(url, params={'reportType': reportType}, timeout=self.timeout)

        except Exception as e:
            print(e)

    def reports_balance(self,
                        timestamp,
                        account=None,
                        counteragent=None,
                        department=None):
        """
        Балансы по счетам, контрагентам и подразделениям

        :param timestamp: учетная-дата время отчета в формате yyyy-MM-dd'T'HH:mm:ss.
        :type timestamp: time
        :param account: (optional)  id счета для фильтрации (можно указать несколько).
        :type timestamp: string
        :param counteragent: (optional) id контрагента для фильтрации (необязательный, можно указать несколько).
        :department: (optional) id подразделения для фильтрации (необязательный, можно указать несколько).
        
        :returns: request
        См. ниже пример результата.

        """
        try:
            urls = self.address + 'reports/balance/counteragents?key=' + self.token
            return requests.get(
                urls,
                params={timestamp, account, counteragent, department},
                timeout=self.timeout)

        except Exception as e:
            print(e)

# ----------------------------------Накладные----------------------------------

    def invoice_in(self, **kwargs):
        """Выгрузка приходных накладных

        :param from: начальная дата (входит в интервал).
        :type from: YYYY-MM-DD
        :param to: конечная  дата (входит в интервал, время не учитывается).
        :type to: YYYY-MM-DD
        :param supplierId: Id поставщика.
        :type supplierId: GUID

        :returns: request
        """
        try:
            urls = self.address + 'api/documents/export/incomingInvoice?key=' + self.token
            return requests.get(
                urls, params=kwargs, timeout=self.timeout)

        except Exception as e:
            print(e)

    def invoice_out(self, **kwargs):
        """Выгрузка расходных накладных

        :param from: начальная дата (входит в интервал).
        :type from: YYYY-MM-DD
        :param to: конечная  дата (входит в интервал, время не учитывается).
        :type to: YYYY-MM-DD
        :param supplierId: Id поставщика.
        :type supplierId: (optional) GUID

        При запросе без постащиков возвращает все расходные накладные, попавшие в интервал.

        :returns: request
        """
        try:
            urls = self.address + 'api/documents/export/outgoingInvoice?key=' + self.token
            return requests.get(
                urls, params=kwargs, timeout=self.timeout)

        except Exception as e:
            print(e)

    def invoice_number_in(self, current_year=True, **kwargs):
        """Выгрузка приходной накладной по ее номеру

        :param number: номер документа.
        :type number: string
        :param from: (optional) начальная дата (входит в интервал).
        :type from: YYYY-MM-DD
        :param to: (optional) конечная  дата (входит в интервал, время не учитывается).
        :type to: YYYY-MM-DD
        :param currentYear: только за текущий год (по умолчанию True).
        :type supplierId: Boolean

        .. note::
            При currentYear = true, вернет документы с указанным номером документа только за текущий год. Параметры from и to должны отсутствовать.

            При currentYear = false параметры from и to должны быть указаны.

        :returns: request

        """

        try:
            urls = self.address + 'api/documents/export/incomingInvoice/byNumber?key=' \
                   + self.token + '&currentYear' + current_year
            return requests.get(
                urls, params=kwargs, timeout=self.timeout)

        except Exception as e:
            print(e)

    def invoice_number_out(self, current_year=True, **kwargs):
        """Выгрузка расходной накладной по ее номеру.


        :param number: номер документа.
        :type number: string
        :param from: (optional) начальная дата (входит в интервал).
        :type from: YYYY-MM-DD
        :param to: (optional) конечная  дата (входит в интервал, время не учитывается).
        :type to: YYYY-MM-DD
        :param currentYear: только за текущий год (по умолчанию True).
        :type supplierId: Boolean

        .. note::
            При currentYear = true, вернет документы с указанным номером документа только за текущий год. Параметры from и to должны отсутствовать.

            При currentYear = false параметры from и to должны быть указаны.
        :returns: request
        """

        try:
            urls = self.address + 'api/documents/export/outgoingInvoice/byNumber?key=' \
                   + self.token + '&currentYear' + current_year
            return requests.get(
                urls, params=kwargs, timeout=self.timeout)

        except Exception as e:
            print(e)

    def production_doc(self, xml):
        """
        Загрузка акта приготовления
        :returns: request
        """
        try:
            target_url = self.address + '/api/documents/import/productionDocument?key' + self.token
            headers = {'Content-type': 'text/xml'}
            return requests.post(
                target_url, body=xml, headers=headers,
                timeout=self.timeout)

        except Exception as e:
            print(e)

# ----------------------------------Получение данных по кассовым сменам:----------------------------------

    def close_session(self, dateFrom=None, dateTo=None):
        """Список кассовых смен

        :param dateFrom: (DD.MM.YYYY) Начальная дата.
        :param dateTo: (DD.MM.YYYY) Конечная дата.

        :returns: request

        """
        try:
            urls = self.address + 'api/closeSession/list?key=' \
                   + self.token
            return requests.get(
                urls, params={dateFrom, dateTo},
                timeout=self.timeout)

        except Exception as e:
            print(e)

    def session(self, from_time=None, to_time=None):
        """Информация о кассовых сменах

        :param from_time: Время с которого запрашиваются данные по кассовым сменам, в формате ISO.
        :type from: yyyy-MM-ddTHH:mm:ss.SSS
        :param to_time:  Время по которое (не включительно) запрашиваются данные по кассовым сменам в формате ISO.
        :type to: yyyy-MM-ddTHH:mm:ss.SSS

        :returns: request

        """
        try:
            urls = self.address + 'api/events/sessions?key=' \
                   + self.token
            return requests.get(
                urls, params={from_time, to_time},
                timeout=self.timeout)

        except Exception as e:
            print(e)

# ----------------------------------EDI----------------------------------

    def edi(self, edi, gln=None, inn=None, kpp=None, name=None):
        """Список заказов для участника EDI senderId и поставщика seller

        :param ediSystem: Идентификатор участника EDI, подключенной к нашему REST API. Каждый участник EDI должен \
            получить свой собственный GUID ключ - идентификатор системы EDI (EdiSystem) для подключения к REST API\
            электронного документооборота iiko. См. "Обмен данными/Системы EDI" в iikoOffce..
        :type ediSystem: GUID
        :param gln: (optional) GLN поставщика . Может отсутствовать, но тогда параметр inn должен быть заполнен.
        :type gln: String
        :param inn: (optional) ИНН (идентификационный номер налогоплательщика). Может отсутствовать, но тогда параметр gln должен быть заполнен.
        :type inn: String
        :param kpp: (optional) КПП (код причины постановки).
        :type kpp: String
        :param name: (optional) Имя поставщика
        :type name: String


        :returns: request

        """

        try:
            urls = self.address + 'edi/' + edi + '/orders/bySeller'
            payload = {'gln': gln, 'inn': inn, 'kpp': kpp, 'name': name}
            return requests.get(
                urls, params=payload, timeout=self.timeout)

        except Exception as e:
            print(e)
