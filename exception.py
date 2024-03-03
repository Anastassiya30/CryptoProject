import json

import requests

from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise APIException(f"Please enter different currencies: {base}.")

        quote_ticker, base_ticker = keys[quote], keys[base]
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f"Cannot enter same currencies: {base}.")
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f"Cannot enter same currencies: {quote}. Please try again")
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Incorrect value: {amount}. Please try again")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}")
        total_base = json.loads(r.content)[keys[quote]]
        total_base = total_base * amount
        return total_base
