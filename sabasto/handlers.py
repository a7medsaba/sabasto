from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from config import *
from database import *

# ----- معالجة أمر /start -----
def start(update, context):
    keyboard = [
        [InlineKeyboardButton("استعراض الأصناف", callback_data="view_categories")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "مرحبًا بك في *متجر سبأ الإلكتروني*.\nاختر من القائمة التي تظهر لك",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ----- معالجة الأزرار (Inline Keyboard) -----
def handle_callback(update, context):
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    # عرض التصنيفات
    if data == "view_categories":
        categories = get_json_data(CATEGORIES_FILE)
        buttons = []
        for category in categories:
            buttons.append([InlineKeyboardButton(
                category["name"],
                callback_data=f"view_category_{category['id']}"
            )])
        reply_markup = InlineKeyboardMarkup(buttons)
        query.edit_message_text(
            text="اختر التصنيف الذي تود استعراضه:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    # عرض المنتجات في التصنيف
    elif data.startswith("view_category_"):
        category_id = int(data.split("_")[-1])
        categories = get_json_data(CATEGORIES_FILE)
        products = get_json_data(PRODUCTS_FILE)
        
        # البحث عن اسم التصنيف
        category_name = next(
            (cat["name"] for cat in categories if cat["id"] == category_id),
            "غير معروف"
        )
        
        # تصفية المنتجات حسب التصنيف
        filtered_products = [p for p in products if p["category_id"] == category_id]
        
        if filtered_products:
            text = f"📦 *أصناف قسم {category_name}*:\n"
            buttons = []
            for product in filtered_products:
                text += f"\n🛍️ *{product['name']}* - {product['price']} ريال\n"
                buttons.append([
                    InlineKeyboardButton("حجز الآن", callback_data=f"order_{product['id']}"),
                    InlineKeyboardButton("أضف للمفضلة", callback_data=f"add_to_favorites_{product['id']}")
                ])
            reply_markup = InlineKeyboardMarkup(buttons)
            query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")
        else:
            query.edit_message_text("لا توجد أصناف في هذا التصنيف.")

    # معالجة طلب الحجز
    elif data.startswith("order_"):
        product_id = int(data.split("_")[1])
        products = get_json_data(PRODUCTS_FILE)
        product = next((p for p in products if p["id"] == product_id), None)
        
        if product:
            context.user_data["pending_order"] = {
                "product_id": product_id,
                "product_name": product["name"],
                "price": product["price"]
            }
            query.edit_message_text(
                f"لقد اخترت المنتج: *{product['name']}*\n"
                "من فضلك أدخل رقم هاتفك لتأكيد الطلب:",
                parse_mode="Markdown"
            )

    # إضافة للمفضلة
    elif data.startswith("add_to_favorites_"):
        product_id = int(data.split("_")[-1])
        chat_id = query.message.chat_id
        favorites = get_json_data(FAVORITES_FILE)
        
        if str(chat_id) not in favorites:
            favorites[str(chat_id)] = []
        
        if product_id not in favorites[str(chat_id)]:
            favorites[str(chat_id)].append(product_id)
            save_json_data(FAVORITES_FILE, favorites)
            query.answer("✅ تم إضافة المنتج للمفضلة.")
        else:
            query.answer("❌ هذا المنتج موجود بالفعل في المفضلة.")

# ----- معالجة رسائل الهاتف (لتأكيد الطلب) -----
def handle_phone(update, context):
    if "pending_order" in context.user_data:
        phone = update.message.text
        orders = get_json_data(ORDERS_FILE)
        
        new_order = {
            **context.user_data["pending_order"],
            "phone": phone,
            "user_chat_id": update.message.chat_id,
            "user_name": update.message.from_user.first_name,
            "status": "منتظر"
        }
        orders.append(new_order)
        save_json_data(ORDERS_FILE, orders)
        
        update.message.reply_text("✅ تم تسجيل طلبك بنجاح، سيتم التواصل معك قريباً.")
        del context.user_data["pending_order"]