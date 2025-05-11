from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from database import Database
from config import ADMIN_USER_ID
from utils.validation import Validator

class AdminHandlers:
    @staticmethod
    def admin_panel(update, context):
        """لوحة تحكم المسؤول الرئيسية"""
        if str(update.message.from_user.id) != ADMIN_USER_ID:
            return

        keyboard = [
            [InlineKeyboardButton("📋 قائمة الطلبات", callback_data="admin_orders")],
            [InlineKeyboardButton("🛍 إدارة المنتجات", callback_data="admin_products")],
            [InlineKeyboardButton("📢 مراجعة العروض", callback_data="admin_offers")],
            [InlineKeyboardButton("💱 إدارة العملات", callback_data="admin_currencies")],
            [InlineKeyboardButton("👥 إدارة المستخدمين", callback_data="admin_users")]
        ]
        update.message.reply_text(
            "🔐 لوحة تحكم المسؤول:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    @staticmethod
    def handle_orders(update, context):
        """إدارة جميع الطلبات"""
        query = update.callback_query
        orders = Database.load_data('orders')
        
        # تصنيف الطلبات حسب الحالة
        pending = [o for o in orders if o['status'] == 'pending']
        completed = [o for o in orders if o['status'] == 'completed']
        
        text = (
            f"📊 إحصائيات الطلبات:\n"
            f"🟡 قيد الانتظار: {len(pending)}\n"
            f"🟢 مكتملة: {len(completed)}\n\n"
            f"استخدم الأوامر التالية:\n"
            f"/pending_orders - لعرض الطلبات قيد الانتظار\n"
            f"/complete_order <رقم_الطلب> - لإكمال الطلب"
        )
        query.edit_message_text(text)

    @staticmethod
    def manage_products(update, context):
        """إدارة المنتجات"""
        query = update.callback_query
        products = Database.load_data('products')
        
        keyboard = [
            [InlineKeyboardButton("➕ إضافة منتج", callback_data="add_product")],
            [InlineKeyboardButton("✏️ تعديل منتج", callback_data="edit_product")],
            [InlineKeyboardButton("🗑 حذف منتج", callback_data="delete_product")],
            [InlineKeyboardButton("📦 جميع المنتجات", callback_data="list_products")]
        ]
        query.edit_message_text(
            "🛍 إدارة المنتجات:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    @staticmethod
    def review_offers(update, context):
        """مراجعة العروض المقدمة"""
        offers = [o for o in Database.load_data('offers') if o['status'] == 'pending']
        
        if not offers:
            update.callback_query.edit_message_text("⚠️ لا توجد عروض قيد المراجعة")
            return

        offer = offers[0]  # نعرض أول عرض في قائمة الانتظار
        user = Database.get_user(offer['user_id'])
        
        text = (
            f"📋 عرض جديد:\n\n"
            f"📌 العنوان: {offer['title']}\n"
            f"📝 الوصف: {offer['description']}\n"
            f"💰 السعر: {offer['price']} {offer['currency']}\n\n"
            f"👤 مقدم العرض:\n"
            f"الاسم: {user['name']}\n"
            f"الهاتف: {user['phone']}"
        )

        keyboard = [
            [InlineKeyboardButton("✅ قبول العرض", callback_data=f"approve_{offer['id']}")],
            [InlineKeyboardButton("❌ رفض العرض", callback_data=f"reject_{offer['id']}")],
            [InlineKeyboardButton("📞 تواصل مع البائع", url=f"https://t.me/{user['username']}")]
        ]
        update.callback_query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    @staticmethod
    def manage_currencies(update, context):
        """إدارة أسعار العملات"""
        query = update.callback_query
        rates = Database.load_data('currencies')['rates']
        
        text = "💱 أسعار العملات الحالية:\n"
        for currency, rate in rates.items():
            text += f"\n{currency}: 1 = {rate} SAR"
        
        text += "\n\nلتحديث سعر عملة:\n/update_rate USD 3.75"
        query.edit_message_text(text)