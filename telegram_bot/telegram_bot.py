import telegram
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater, MessageHandler

#  from telegram.ext.filters import Filters
from telegram_bot.views import echo

bot = telegram.Bot(token="6121382783:AAExuYESoAEE8-KZl5r9NgjBlEVyqXvChik")


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    text = """ Hello! I am a bot of our website. To start, choose the language in which you want to receive messages:
    /eng - English language
    /ukr - Українська мова
    /thai - ภาษาไทย
    /fre - Langue française
    /ita - Lingua italiana
    /rus - Русский язык
    /ger - Deutsche Sprache
    """
    update.message.reply_text(text)


def language_eng(update: Update, context: CallbackContext) -> None:
    """Set the language to English."""
    context.user_data["language"] = "eng"
    text = """
    You have chosen English language. 
        On our website, we offer services for selecting a friendly local 
    who is ready to help you solve problems for a modest fee. 
        Thanks to their many years of experience on the island and their
    rich knowledge of local culture, they can offer you the best solutions
    and tips for quick and effective problem-solving, including motorcycle rental,
    training, medical assistance, or translations, as well as convenient shopping 
    for directions: clothes, delicious food or souvenirs, so you can enjoy everything 
    our island has to offer. 
        Additionally, you can add your skills and abilities to our database for service provision.
    Here is the link to our website: {site_url}
    """.format(
        site_url=settings.SITE_URL
    )
    update.message.reply_text(text)


def language_ukr(update: Update, context: CallbackContext) -> None:
    """Set the language to Ukrainian."""
    context.user_data["language"] = "ukr"
    text = """
    Ви вибрали українську мову.
        На нашому сайті ми пропонуємо послуги з підбору дружнього аборигена,
    який готовий допомогти вам у вирішенні проблем за скромну винагороду.
        Завдяки його багаторічному досвіду на острові та глибокому 
    знанню місцевої культури, він зможе запропонувати вам найкращі рішення та поради для 
    швидкого та ефективного вирішення будь-яких проблем, включаючи оренду мотоцикла,
    навчання, медичну допомогу або переклади, а також зручний шопінг 
    за напрямами: одяг, смачна їжа або сувеніри, щоб ви могли насолоджуватися усім,
    що наш острів може запропонувати. 
         Також ви можете додати свої навички та можливості до бази даних для надання послуг.
    Ось посилання на наш сайт: {site_url}
    """.format(
        site_url=settings.SITE_URL
    )
    update.message.reply_text(text)


def language_thai(update: Update, context: CallbackContext) -> None:
    """Set the language to Thai."""
    context.user_data["language"] = "thai"
    text = """
    คุณได้เลือกภาษาไทยแล้ว ภาษาไทย: 
    บนเว็บไซต์ของเราเรามีบริการเลือกคนบ้านที่เป็นมิตรที่พร้อมช่วยคุณแก้ปัญหาโดยรับค่าตอบแทนที่เบาๆ
    ด้วยประสบการณ์หลายปีในเกาะและความรู้ท้องถิ่นที่มั่นใจ 
    เขาสามารถให้ข้อเสนอแนะที่ดีที่สุดและเคล็ดลับสำหรับการแก้ปัญหาอย่างรวดเร็วและมีประสิทธิภาพสำหรับปัญหาใดๆ
    รวมถึงการเช่ามอเตอร์ไซค์การฝึกอบรมการดูแลสุขภาพหรือการแปลภาษาและการช้อปปิ้งที่สะดวกสบาย
    สำหรับการช้อปปิ้งสำหรับเสื้อผ้าอาหารอร่อยหรือของฝากเพื่อให้คุณสามารถเพลิดเพลินไปกับทุกสิ่งที่เกาะของเรามีเสนอได้อย่างสะดวกสบาย 
    นอกจากนี้คุณยังสามารถเพิ่มทักษะและความสามารถของคุณในฐานข้อมูลเพื่อให้บริการได้
    นี่คือลิงก์ไปยังเว็บไซต์ของเรา: {site_url}
    """.format(
        site_url=settings.SITE_URL
    )
    update.message.reply_text(text)


def language_fre(update: Update, context: CallbackContext) -> None:
    """Set the language to French."""
    context.user_data["language"] = "fre"
    text = """ Vous avez choisi la langue française.
        Sur notre site web, nous offrons des services de sélection d'un
    autochtone amical prêt à vous aider à résoudre des problèmes moyennant 
    une somme modeste. Grâce à leur expérience de plusieurs années sur l'île
    et à leur riche connaissance de la culture locale, ils peuvent vous offrir 
    les meilleures solutions et astuces pour résoudre rapidement et efficacement
    tous les problèmes, y compris la location de motos, la formation, 
    l'assistance médicale ou les traductions, ainsi que des achats pratiques
    Voici le lien vers notre site web: {site_url}
    """.format(
        site_url=settings.SITE_URL
    )
    update.message.reply_text(text)


def language_ita(update: Update, context: CallbackContext) -> None:
    """Set the language to Italian."""
    context.user_data["language"] = "ita"
    text = """Hai scelto la lingua italiana.
        Sul nostro sito offriamo servizi di ricerca di un amichevole aborigeno,
    pronto ad aiutarti a risolvere i problemi in cambio di una modesta ricompensa. 
    Grazie alla sua lunga esperienza sull'isola e alla sua vasta conoscenza della 
    cultura locale, sarà in grado di offrirti le migliori soluzioni e suggerimenti
    per risolvere rapidamente ed efficacemente qualsiasi problema, tra cui noleggio 
    di moto, formazione, assistenza sanitaria o traduzioni, nonché comodo shopping 
    in aree come abbigliamento, cibo delizioso o souvenir, in modo da poter goderti
    tutto ciò che la nostra isola ha da offrire.
        Puoi anche inserire le tue competenze e le tue opportunità
    nel nostro database per fornire servizi."
    Ecco il link al nostro sito web: {site_url}
    """.format(
        site_url=settings.SITE_URL
    )
    update.message.reply_text(text)


def language_rus(update: Update, context: CallbackContext) -> None:
    """Set the language to Russian."""
    context.user_data["language"] = "rus"
    text = """Вы выбрали русский язык. 
        На нашем сайте мы предлагаем услуги по подбору дружелюбного аборигена,
    который готов помочь вам в решении проблем за скромное вознаграждение. 
    Благодаря его многолетнему опыту на острове и богатому знанию местной культуры, 
    он сможет предложить вам лучшие решения и подсказки для быстрого и эффективного
    решения любых проблем, включая мотоаренду, обучение, медицинскую помощь или переводы,
    а также удобный шопинг по направлениям: одежда, вкусная еда или сувениры, чтобы вы могли 
    наслаждаться всем, что наш остров может предложить. 
        Также вы можете внести свои навыки и возможности в базу данных для предоставления услуг
    Вот ссылка на наш сайт: {site_url}
    """.format(
        site_url=settings.SITE_URL
    )
    update.message.reply_text(text)


def language_ger(update: Update, context: CallbackContext) -> None:
    """Set the language to German."""
    context.user_data["language"] = "ger"
    text = """Sie haben die deutsche Sprache gewählt.
        Auf unserer Website bieten wir Dienstleistungen zur Suche nach einem 
    freundlichen Ureinwohner an, der bereit ist, Ihnen gegen eine bescheidene 
    Vergütung bei der Lösung von Problemen zu helfen. Dank seiner langjährigen 
    Erfahrung auf der Insel und seinem umfangreichen Wissen über die lokale 
    Kultur kann er Ihnen die besten Lösungen und Tipps zur schnellen und effektiven
    Lösung aller Arten von Problemen anbieten, einschließlich Motorradvermietung, 
    Schulungen, medizinische Versorgung oder Übersetzungen sowie bequemes Einkaufen 
    in Bereichen wie Kleidung, leckeres Essen oder Souvenirs, damit Sie alles 
    genießen können, was unsere Insel zu bieten hat.
        Sie können auch Ihre Fähigkeiten und Möglichkeiten in unsere Datenbank
    eingeben, um Dienstleistungen anzubieten."
    Hier ist der Link zu unserer Website: {site_url}
    """.format(
        site_url=settings.SITE_URL
    )
    update.message.reply_text(text)


@csrf_exempt
def telegram_webhook(request):
    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
    update = telegram.Update.de_json(request.body, bot)
    dispatcher = Updater(bot.token, use_context=True).dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("rus", language_rus))
    dispatcher.add_handler(CommandHandler("ukr", language_ukr))
    dispatcher.add_handler(CommandHandler("thai", language_thai))
    dispatcher.add_handler(CommandHandler("eng", language_eng))
    dispatcher.add_handler(CommandHandler("fre", language_fre))
    dispatcher.add_handler(CommandHandler("ita", language_ita))
    dispatcher.add_handler(CommandHandler("ger", language_ger))
    dispatcher.process_update(update)
    return HttpResponse(status=200)


# Функция для настройки webhook
def set_webhook():
    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
    url = settings.WEBHOOK_URL

    # Удаление предыдущего вебхука, если он был настроен
    bot.delete_webhook()

    # Установка нового вебхука
    bot.set_webhook(url=url)

    return HttpResponse("Webhook настроен успешно.")


# Функция-обработчик входящих сообщений
@csrf_exempt
def webhook(request):
    # Создание объекта Updater для получения входящих сообщений
    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
    updater = Updater(bot=bot, use_context=True)

    # Регистрация функций-обработчиков команд и сообщений
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    #   dp.add_handler(MessageHandler(Filters.text, echo))

    # Получение входящего сообщения и его обработка
    update = telegram.Update.de_json(request.body, bot)
    dp.process_update(update)

    return HttpResponse("OK.")
