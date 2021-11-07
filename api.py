import time
from urllib.parse import urlencode

import requests

from helpers import hash_by_sha256, hash_by_md5


class FreekassaApi:
    API_BASE_URL = 'https://api.freekassa.ru/v1/{method}'
    PAYMENT_BASE_URL = 'https://pay.freekassa.ru/?{query}'

    def __init__(self, shop_id: int, secret1: str, secret2: str, api_key: str):
        self.session = requests.Session()

        self.shop_id = shop_id
        self.secret1 = secret1
        self.secret2 = secret2
        self.api_key = api_key

    def _generate_api_signature(self, json: dict) -> str:
        sorted_values = []

        for key in sorted(json.keys()):
            sorted_values.append(str(json[key]))

        return hash_by_sha256(self.api_key, '|'.join(sorted_values))

    def generate_payment_form_signature(self, amount: int, order_id: str, currency='RUB') -> str:
        return hash_by_md5(f'{self.shop_id}:{amount}:{self.secret1}:{currency}:{order_id}')

    def request(self, method: str, json: dict = None) -> dict:
        url = self.API_BASE_URL.format(method=method)

        json = json or {}
        json = {k: v for k, v in json.items() if v is not None}
        json = {**json, 'shopId': self.shop_id, 'nonce': time.time_ns()}
        json = {**json, 'signature': self._generate_api_signature(json)}

        resp = self.session.post(url, json=json)
        return resp.json()


class Merchant(FreekassaApi):

    def balance(self) -> dict:
        return self.request('balance')

    def get_payment_url(self, amount: int, payment_id: str, currency='RUB',
                        payment_method: int = None, phone: str = None, email: str = None, lang: str = None) -> str:
        params = {
            'm': self.shop_id,
            'oa': amount,
            'currency': currency,
            'o': payment_id,
            's': self.generate_payment_form_signature(amount, payment_id, currency),
            'i': payment_method,
            'phone': phone,
            'em': email,
            'lang': lang,
        }
        payload = {k: v for k, v in params.items() if v is not None}
        return self.PAYMENT_BASE_URL.format(query=urlencode(payload))

    def orders(self, order_id: int = None, payment_id: str = None, order_status: int = None,
               date_from: str = None, date_to: str = None, page: int = None):
        json = {
            'orderId': order_id,
            'paymentId': payment_id,
            'orderStatus': order_status,
            'dateFrom': date_from,
            'dateTo': date_to,
            'page': page,
        }
        return self.request('orders', json)

    def create_order(self, i: int, email: str, ip: str, amount: int, currency: str = 'RUB',
                     payment_id: str = None, tel: str = None):
        json = {
            'i': i,
            'email': email,
            'ip': ip,
            'amount': amount,
            'currency': currency,
            'paymentId': payment_id,
            'tel': tel,
        }
        return self.request('orders/create', json)

    def currencies(self):
        return self.request('currencies')

    def currency_status(self, payment_method: int):
        return self.request(f'currencies/{payment_method}/status')

    def shops(self):
        return self.request('shops')
