from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

def enter_phone_number(update, context):
    user = update.message.from_user
    chat_id = update.message.chat_id
    context.user_data['phone_number'] = None  # Инициализируем поле в контексте пользователя

    reply_keyboard = [['Отправить свой номер телефона'], ['Отмена']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    update.message.reply_text(
        'Для продолжения авторизации необходимо отправить свой номер телефона. Нажмите кнопку ниже:',
        reply_markup=markup,
    )

    return PHONE_NUMBER


def receive_phone_number(update, context):
    user = update.message.from_user
    chat_id = update.message.chat_id
    phone_number = update.message.contact.phone_number

    # Сохраняем номер телефона в базу данных Django, связав его с текущим пользователем (Visitor)
    visitor = Visitor.objects.get(userNick=user.username)
    visitor.phone_number = phone_number
    visitor.save()

    update.message.reply_text(
        'Спасибо! Теперь введите пароль для продолжения авторизации:',
    )

    return PASSWORD
Пример кода для функции enter_password:

python
Copy code
def enter_password(update, context):
    user = update.message.from_user
    chat_id = update.message.chat_id
    context.user_data['password'] = None  # Инициализируем поле в контексте пользователя

    update.message.reply_text(
        'Введите пароль для продолжения авторизации:',
    )

    return PASSWORD


def receive_password(update, context):
    user = update.message.from_user
    chat_id = update.message.chat_id
    password = update.message.text

    # Сохраняем пароль в базу данных Django, связав его с текущим пользователем (Visitor)
    visitor = Visitor.objects.get(userNick=user.username)
    visitor.password = password
    visitor.save()

    update.message.reply_text(
        'Вы успешно авторизовались! Теперь вы можете пользоваться ботом.',
    )

    return ConversationHandler.END

# определяем состояния диалога
PHONE_NUMBER, PASSWORD = range(2)

# функция-обработчик для команды /start
def start(update, context):
    # отправляем пользователю приветственное сообщение
    update.message.reply_text("Добро пожаловать! Пожалуйста, введите свой номер телефона.")
    # переходим в состояние PHONE_NUMBER
    return PHONE_NUMBER

# функция-обработчик для получения номера телефона
def get_phone_number(update, context):
    # получаем номер телефона, введенный пользователем
    phone_number = update.message.text
    # сохраняем номер телефона в контексте
    context.user_data['phone_number'] = phone_number
    # запрашиваем пароль
    update.message.reply_text("Отлично! Теперь введите пароль.")
    # переходим в состояние PASSWORD
    return PASSWORD

# функция-обработчик для получения пароля
def get_password(update, context):
    # получаем пароль, введенный пользователем
    password = update.message.text
    # сохраняем пароль в контексте
    context.user_data['password'] = password
    # выводим сообщение об успешной авторизации
    update.message.reply_text("Спасибо! Вы успешно авторизовались.")
    # сбрасываем состояние диалога
    return ConversationHandler.END

# функция-обработчик для отмены диалога
def cancel(update, context):
    # выводим сообщение об отмене
    update.message.reply_text("Действие отменено.")
    # сбрасываем состояние диалога
    return ConversationHandler.END

# создаем объект ConversationHandler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        PHONE_NUMBER: [MessageHandler(Filters.text & ~Filters.command, get_phone_number)],
        PASSWORD: [MessageHandler(Filters.text & ~Filters.command, get_password)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

# добавляем обработчик в диспетчер Telegram
dispatcher.add_handler(conv_handler)
