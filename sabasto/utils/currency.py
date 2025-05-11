from config import DEFAULT_CURRENCY, CURRENCY_RATES
from datetime import datetime

class CurrencyConverter:
    @staticmethod
    def convert(amount, from_currency, to_currency=DEFAULT_CURRENCY):
        """تحويل العملات مع تحديث الأسعار"""
        if from_currency == to_currency:
            return amount
        
        rate = CURRENCY_RATES.get(from_currency, 1)
        return round(amount * rate, 2)

    @staticmethod
    def format_price(amount, currency):
        """تنسيق السعر مع رمز العملة"""
        symbols = {
            "SAR": "﷼",
            "USD": "$",
            "EUR": "€"
        }
        return f"{symbols.get(currency, currency)} {amount}"