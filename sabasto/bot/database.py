import json
import os
from config import FILE_PATHS
from datetime import datetime

class Database:
    @staticmethod
    def load_data(file_key):
        """تحميل بيانات JSON"""
        try:
            with open(FILE_PATHS[file_key], 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {} if file_key in ['users', 'favorites'] else []

    @staticmethod
    def save_data(file_key, data):
        """حفظ البيانات في ملف JSON"""
        with open(FILE_PATHS[file_key], 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def get_next_id(items):
        """إنشاء ID فريد"""
        return max(item['id'] for item in items) + 1 if items else 1

    @staticmethod
    def get_user(user_id):
        """استرجاع بيانات مستخدم"""
        users = Database.load_data('users')
        return users.get(str(user_id))

    @staticmethod
    def register_user(user_data):
        """تسجيل مستخدم جديد"""
        users = Database.load_data('users')
        users[str(user_data['user_id'])] = user_data
        Database.save_data('users', users)