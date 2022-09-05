import requests
import json
from config import currency

class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: float):
        # Preventing from choose the same currency to convert
        if quote == base:
            raise ConvertionException("You picked the same currency, try again.")
        quote_ticker = currency[quote]
        base_ticker = currency[base]

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise ConvertionException(f"Can not process {quote}.")

        try:
            base_ticker = currency[base]
        except KeyError:
            raise ConvertionException(f"Can not process {base}.")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Can not to process your {amount}.")

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[currency[base]]

        return total_base * float(amount)
