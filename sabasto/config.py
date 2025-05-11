import os
from datetime import datetime

# التوكن والإعدادات
BOT_TOKEN = os.getenv("BOT_TOKEN", "7646983713:AAEsQVDD0aPKAr_cLJ8xxvefXcTw7unylRg")
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID", "5896443755")

# مسارات الملفات
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

FILE_PATHS = {
    "users": os.path.join(DATA_DIR, "users.json"),
    "categories": os.path.join(DATA_DIR, "categories.json"),
    "products": os.path.join(DATA_DIR, "products.json"),
    "orders": os.path.join(DATA_DIR, "orders.json"),
    "favorites": os.path.join(DATA_DIR, "favorites.json"),
    "offers": os.path.join(DATA_DIR, "offers.json"),
    "currencies": os.path.join(DATA_DIR, "currencies.json")
}

# إعدادات العملة
DEFAULT_CURRENCY = "SAR"
CURRENCY_RATES = {
    "USD": 3.75,
    "EUR": 4.20
}

# حدود النظام
MAX_PRODUCT_IMAGES = 5
MAX_OFFER_FILES = 3
OFFER_EXPIRY_DAYS = 30  # مدة صلاحية العرض
