import os
import telebot
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    MessageHandler,
    Filters
)

class CS2ShopBot:
    def __init__(self, token: str):
        self.token = token
        self.items = {
            'ice_coal': {
                'name': '❄️ Ледяной уголь',
                'price': 700,
                'image': 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpot621FAR17PLfYQJH5d2zhr-ZkvD8J_WDkjlVvZJ03O3A9I_j3Qew_BY_ZGG1JY-Sd1I_MFjX-lTqk-nq1pO_v8jLn3Jg7HIl5XfDn1a3iBAdPw/360fx360f',
                'desc': 'Эксклюзивный узор для ножей'
            },
            'redline': {
                'name': '🔴 AK-47 | Красная линия',
                'price': 1500,
                'image': 'https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpou-6kejhz2v_Nfz5H_uO1gb-Gm_b5J4Tdn2xZ_Pp9jL2Uod-h3Fbk_RY_YTqhI4-Hcgc9Z1nW-QS6xO3p0Za5vJnNzHJ9-nRztynbl0e2iBodPw/360fx360f',
                'desc': 'Легендарный скин для AK-47'
            }
        }

    def start(self, update: Update, context: CallbackContext) -> None:
        """Обработчик команды /start"""
        buttons = [
            [InlineKeyboardButton(item['name'], callback_data=f"item_{item_id}")]
            for item_id, item in self.items.items()
        ]
        
        update.message.reply_text(
            "🎮 Добро пожаловать в магазин CS2!\nВыберите предмет:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    def show_item(self, update: Update, context: CallbackContext) -> None:
        """Показ выбранного предмета"""
        query = update.callback_query
        query.answer()
        
        item_id = query.data.split('_')[1]
        item = self.items.get(item_id)
        
        if not item:
            query.edit_message_text("⚠️ Предмет не найден")
            return
        
        keyboard = [
            [InlineKeyboardButton("💰 Купить", callback_data=f"buy_{item_id}")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back")]
        ]
        
        context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=item['image'],
            caption=f"{item['name']}\n\n{item['desc']}\n\nЦена: {item['price']} монет",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        query.delete_message()

    def process_purchase(self, update: Update, context: CallbackContext) -> None:
        """Обработка покупки"""
        query = update.callback_query
        query.answer()
        
        item_id = query.data.split('_')[1]
        item = self.items.get(item_id)
        
        if item:
            query.edit_message_caption(
                caption=f"✅ Вы купили {item['name']} за {item['price']} монет!")
        else:
            query.edit_message_text("⚠️ Ошибка при покупке")

    def back_to_menu(self, update: Update, context: CallbackContext) -> None:
        """Возврат в главное меню"""
        query = update.callback_query
        query.answer()
        
        buttons = [
            [InlineKeyboardButton(item['name'], callback_data=f"item_{item_id}")]
            for item_id, item in self.items.items()
        ]
        
        query.edit_message_text(
            "Выберите предмет:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    def run(self) -> None:
        """Запуск бота"""
        updater = Updater(self.token)
        dp = updater.dispatcher

        # Регистрация обработчиков
        dp.add_handler(CommandHandler('start', self.start))
        dp.add_handler(CallbackQueryHandler(self.show_item, pattern='^item_'))
        dp.add_handler(CallbackQueryHandler(self.process_purchase, pattern='^buy_'))
        dp.add_handler(CallbackQueryHandler(self.back_to_menu, pattern='^back$'))
        
        # Обработка текстовых сообщений
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.start))
        
        updater.start_polling()
        updater.idle()

if __name__ == '__main__':
    # Укажите ваш токен бота
    TOKEN = os.getenv('7628176412:AAFm_vPxSx_YemqjZ_V8BKY9QdFf_qoUYTY') or '7628176412:AAFm_vPxSx_YemqjZ_V8BKY9QdFf_qoUYTY'
    
    bot = CS2ShopBot(TOKEN)
    bot.run()