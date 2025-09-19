import os
import logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота из переменных окружения
BOT_TOKEN = ('7701273865:AAHZn4XK245nb-v9sWxx74zOeWGm1Il72lc')

if not BOT_TOKEN:
    raise ValueError("Необходимо указать BOT_TOKEN в файле .env")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    
    welcome_text = f"""
👋 Привет, {user.first_name}!

Добро пожаловать в SapsanVPN - ваш надежный VPN сервис для безопасного и быстрого интернета.

🔒 Безопасность и анонимность
🌍 Доступ к заблокированным сайтам
⚡ Высокая скорость соединения
📱 Работает на всех устройствах

Используйте команду /webapp для открытия приложения.
    """
    
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_text = """
📖 SapsanVPN - Справка

🔧 Доступные команды:
/start - Приветствие и информация о сервисе
/webapp - Открыть веб-приложение

💡 О сервисе:
SapsanVPN обеспечивает безопасное и быстрое подключение к интернету с возможностью обхода блокировок и защиты личных данных.

Для начала работы используйте команду /webapp.
    """
    await update.message.reply_text(help_text)

async def webapp_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /webapp"""
    keyboard = [
        [InlineKeyboardButton(
            "🚀 Открыть SapsanVPN", 
            web_app=WebAppInfo(url="https://xpressvision.online/webapp.html")
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🌐 Откройте приложение SapsanVPN для управления VPN подключением:",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на inline кнопки"""
    query = update.callback_query
    await query.answer()
    
    # Убираем обработку кнопки помощи, так как её больше нет
    pass

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.warning(f'Update {update} caused error {context.error}')

def main() -> None:
    """Основная функция запуска бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("webapp", webapp_command))
    
    # Добавляем обработчик callback кнопок
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    print("🤖 Бот запущен! Нажмите Ctrl+C для остановки.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

