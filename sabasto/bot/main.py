from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from handlers.auth import AuthHandlers, GET_NAME, GET_PHONE
from handlers.user import UserHandlers
from handlers.admin import AdminHandlers
from handlers.offers import OfferHandlers
from config import BOT_TOKEN

def setup_handlers(dp):
    # نظام التسجيل
    conv_auth = ConversationHandler(
        entry_points=[CommandHandler('register', AuthHandlers.start_registration)],
        states={
            GET_NAME: [MessageHandler(Filters.text & ~Filters.command, AuthHandlers.get_name)],
            GET_PHONE: [
                MessageHandler(Filters.contact, AuthHandlers.get_phone),
                MessageHandler(Filters.text & ~Filters.command, AuthHandlers.get_phone)
            ],
        },
        fallbacks=[]
    )
    dp.add_handler(conv_auth)

    # أوامر المستخدمين
    dp.add_handler(CommandHandler('start', UserHandlers.start))
    dp.add_handler(CallbackQueryHandler(UserHandlers.handle_callbacks))

    # نظام العروض
    dp.add_handler(CommandHandler('offer', OfferHandlers.start_offer))
    dp.add_handler(MessageHandler(Filters.photo | Filters.document, OfferHandlers.handle_files))

    # أوامر المسؤول
    dp.add_handler(CommandHandler('admin', AdminHandlers.admin_panel))

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    setup_handlers(dp)
    
    updater.start_polling()
    print("🤖 Bot is running...")
    updater.idle()

if __name__ == "__main__":
    main()