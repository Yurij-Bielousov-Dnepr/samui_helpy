from django.shortcuts import render
import telegram
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import logging

logger = logging.getLogger(__name__)
TOKEN = "6121382783:AAExuYESoAEE8-KZl5r9NgjBlEVyqXvChik"

# Инициализируйте телеграм-бота и диспетчера
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0)


# Обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот.")


# Обработчик текстовых сообщений
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


# Функция для настройки вебхука
@require_POST
@csrf_exempt
def webhook(request):
    if request.method == "POST":
        # Преобразование входящего JSON-объекта в объект Telegram Update
        update = telegram.Update.de_json(request.body, bot)

        # Передача Update диспетчеру для обработки
        dispatcher.process_update(update)

        # Возвращаем ответ серверу Telegram
        return HttpResponse(status=200)
    else:
        # Возвращаем ошибку "Метод не поддерживается"
        return HttpResponse(status=405)


# Регистрация обработчиков команд и сообщений
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text, echo))


def telegram_bot(request):
    if request.method == "POST":
        # Получите данные, отправленные пользователем из формы
        chat_id = request.POST.get("chat_id")
        message_text = request.POST.get("message_text")

        # Инициализируйте телеграм-бота с помощью токена бота
        bot = telegram.Bot(token="6055423350:AAHOxcGzuCEeLxWOudMZHty_fiwqSTc0NJQ")

        # Отправьте сообщение пользователю
        bot.send_message(chat_id=chat_id, text=message_text)

    return render(request, "helpy/telegram_bot.html")
