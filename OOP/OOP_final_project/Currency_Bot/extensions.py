import requests
import json
from config import currency


class APIException(Exception):
    pass


class ValuesConverter:
    @staticmethod
    def get_price(quote, base, amount):

        if quote == base:
            raise APIException('Валюты совпадают. Конвертация невозможна. Пожалуйста введите корректные данные.')
        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {quote}.')
        try:
            base_ticker = currency[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {base}.')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество валюты: {amount}.')

        r = requests.get(
            f'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{quote_ticker}.json')
        base_value = json.loads(r.content)[quote_ticker]
        total_base = round(base_value.get(f'{base_ticker}') * amount, 2)
        return total_base
