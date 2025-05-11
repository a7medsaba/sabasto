from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from database import Database
from utils.currency import CurrencyConverter

class ProductHandlers:
    @staticmethod
    def show_product(update, product_id):
        """عرض تفاصيل المنتج"""
        product = next((p for p in Database.load_data('products') if p['id'] == product_id), None)
        if not product:
            return

        converted_price = CurrencyConverter.convert(
            product['price'],
            product.get('currency', 'SAR')
        )

        text = (
            f"🛍 *{product['name']}*\n\n"
            f"💰 السعر: {CurrencyConverter.format_price(product['price'], product.get('currency', 'SAR'))}\n"
            f"   (~{CurrencyConverter.format_price(converted_price, 'SAR')})\n\n"
            f"📝 الوصف: {product.get('description', '')}"
        )

        keyboard = [
            [InlineKeyboardButton("حجز", callback_data=f"order_{product_id}")]
        ]
        return text, InlineKeyboardMarkup(keyboard)