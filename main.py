import json
import os
import asyncio
import logging
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ReplyKeyboardMarkup, KeyboardButton, LabeledPrice
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, PreCheckoutQueryHandler
from telegram.error import TelegramError
print(f"Loaded BOT_TOKEN: {BOT_TOKEN}")
# Load environment variables
load_dotenv()

# Enableasync def check_subscriptions(context: ContextTypes.DEFAULT_TYPE):
admin_id = 1443301925  # твой ID
    
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration

ADMIN_ID = 1443301925
NOTIFICATION_CHAT = "-1002085087426"
DATA_FILE = "bot_data.json"

# Language configurations
LANGUAGES = {
    'en': {
        'welcome': "🎉 Welcome! Please choose your language:",
        'language_changed': "✅ Language changed to English",
        'main_menu': "☰ Main Menu",
        'menu_button': "☰ Menu",
        'balance': "📊 Balance",
        'gift_shop': "🛍️ Gift Shop",
        'change_language': "Change Language",
        'tasks': "📝 Tasks",
        'restart_bot': "🔁 Restart Bot",
        'referral': "🔗 Referral",
        'premium': "💎 Premium",
        'mini_games': "🎮 Mini-Games",
        'farm_stars': "🚀 Farm Stars & Views",
        'bot_restarted': "✅ Bot successfully restarted.",
        'your_balance': "💰 Your balance: {stars} ⭐\n👁️ Views: {views}",
        'no_tasks': "✅ No tasks available at the moment",
        'task_subscribe': "📢 Subscribe to this channel: {channel}\n\nAfter subscribing, press 'Done'",
        'task_done': "✅ Done",
        'task_completed': "🎉 Task completed! +{reward} ⭐ added to your balance",
        'task_not_subscribed': "❌ You didn't subscribe to the channel. Your reward was not credited. Please subscribe to get your stars.",
        'gift_heart': "❤️ Heart - 20 ⭐",
        'gift_box': "🎁 Box - 20 ⭐",
        'gift_rose': "🌹 Rose - 100 ⭐",
        'gift_ring': "💍 Ring - 100 ⭐",
        'insufficient_stars': "❌ Insufficient stars. You need {needed} ⭐",
        'insufficient_requirements': "❌ Insufficient requirements:\n• Referrals: {user_refs}/{req_refs}\n• Views: {user_views}/{req_views}\n• Stars: {user_stars}/{req_stars} ⭐",
        'gift_requested': "✅ Gift request sent! Processing within 1-2 days",
        'admin_only': "❌ Admin access only",
        'admin_help': "Admin commands:\n/admin add <@username|user_id> <amount> <reason>\n/admin remove <@username|user_id> <amount> <reason>\n/admin ban <@username|user_id> <reason>\n/admin new <reward_stars> <task_description> <verification_link>\n/admin stats",
        'user_not_found': "❌ User not found",
        'stars_added': "✅ {amount} ⭐ added to user {user_id}",
        'stars_removed': "✅ {amount} ⭐ removed from user {user_id}",
        'user_banned': "✅ User {user_id} has been banned",
        'you_are_banned': "❌ You have been banned from using this bot",
        'back': "⬅️ Back",
        'unsubscribed_penalty': "❌ You unsubscribed from {channel} within 7 days. {stars} ⭐ have been removed from your balance.",
        'welcome_back': "🎉 Welcome back! Your data has been restored.",
        'referral_info': "🔗 Your referral link:\n{link}\n\n💰 You earn +{reward} ⭐ for each user who joins!\n👥 Referred users: {count}",
        'referral_bonus': "🎉 You got +{stars} ⭐ for inviting a new user!",
        'welcome_bonus': "🎉 Welcome! You got +{stars} ⭐ bonus for joining via referral!",
        'already_referred': "❌ You were already referred by someone else.",
        'premium_info': "💎 Premium Benefits:\n\n🔗 Referral: +7 ⭐ per user (instead of +3)\n👤 New users get: +3 ⭐ (instead of +1)\n📝 Tasks: +1 ⭐ per task (instead of +0.40)\n\n⏰ Duration: 30 days\n💰 Price: 100 Telegram Stars",
        'buy_premium': "💎 Buy Premium",
        'premium_active': "✅ Premium is active until: {date}",
        'premium_expired': "❌ Your premium has expired",
        'slot_machine': "🎰 Slot Machine",
        'fishing_game': "🎣 Fishing Game",
        'slot_bet': "🎰 Choose your bet:",
        'slot_result_win': "🎉 JACKPOT! 777\nYou won {amount} ⭐!",
        'slot_result_lose': "😢 {result}\nYou lost {bet} ⭐",
        'fishing_choose': "🎣 Choose your fishing method:",
        'fishing_garpoon': "🔱 Garpoon (Best)",
        'fishing_rod': "🎣 Rod (Medium)",
        'fishing_hands': "✋ Bare Hands (Low)",
        'fishing_cooldown': "⏰ You need to wait {hours}h {minutes}m before fishing again",
        'fishing_result': "🎣 You caught {amount} ⭐ using {method}!",
        'fishing_nothing': "😞 You caught nothing this time...",
        'insufficient_for_bet': "❌ Insufficient stars for this bet. You have {balance} ⭐",
        'farm_cooldown': "⏰ You need to wait {hours}h {minutes}m before farming again",
        'farm_reward': "🎉 You farmed {stars} ⭐ and got +1 view!\n\nNow complete this task to confirm your reward:",
        'farm_task_completed': "✅ Task completed! Your {stars} ⭐ and view have been confirmed!"
    },
    'ru': {
        'welcome': "🎉 Добро пожаловать! Выберите ваш язык:",
        'language_changed': "✅ Язык изменён на русский",
        'main_menu': "☰ Главное меню",
        'menu_button': "☰ Меню",
        'balance': "📊 Баланс",
        'gift_shop': "🛍️ Магазин подарков",
        'change_language': "🌐 Изменить язык",
        'tasks': "📝 Задания",
        'restart_bot': "🔁 Перезапустить бота",
        'referral': "🔗 Реферальная система",
        'premium': "💎 Премиум",
        'mini_games': "🎮 Мини-игры",
        'farm_stars': "🚀 Фарм звёзд и просмотров",
        'bot_restarted': "✅ Бот успешно перезапущен.",
        'your_balance': "💰 Ваш баланс: {stars} ⭐\n👁️ Просмотры: {views}",
        'no_tasks': "✅ Нет доступных заданий",
        'task_subscribe': "📢 Подпишитесь на канал: {channel}\n\nПосле подписки нажмите 'Готово'",
        'task_done': "✅ Готово",
        'task_completed': "🎉 Задание выполнено! +{reward} ⭐ добавлено",
        'task_not_subscribed': "❌ Вы не подписались на канал. Награда не начислена. Подпишитесь, чтобы получить звёзды.",
        'gift_heart': "❤️ Сердце - 20 ⭐",
        'gift_box': "🎁 Коробка - 20 ⭐",
        'gift_rose': "🌹 Роза - 100 ⭐",
        'gift_ring': "💍 Кольцо - 100 ⭐",
        'insufficient_stars': "❌ Недостаточно звёзд. Нужно {needed} ⭐",
        'insufficient_requirements': "❌ Недостаточно требований:\n• Рефералы: {user_refs}/{req_refs}\n• Просмотры: {user_views}/{req_views}\n• Звёзды: {user_stars}/{req_stars} ⭐",
        'gift_requested': "✅ Запрос отправлен! Обработка в течение 1-2 дней",
        'admin_only': "❌ Только для администратора",
        'admin_help': "Команды администратора:\n/admin add <user_id> <amount> <reason>\n/admin remove <user_id> <amount> <reason>\n/admin ban <user_id> <reason>\n/admin new <reward_stars> <task_description> <verification_link>\n/admin stats",
        'user_not_found': "❌ Пользователь не найден",
        'stars_added': "✅ {amount} ⭐ добавлено пользователю {user_id}",
        'stars_removed': "✅ {amount} ⭐ убрано у пользователя {user_id}",
        'user_banned': "✅ Пользователь {user_id} заблокирован",
        'you_are_banned': "❌ Вы заблокированы и не можете использовать бота",
        'back': "⬅️ Назад",
        'unsubscribed_penalty': "❌ Вы отписались от {channel} в течение 7 дней. {stars} ⭐ списано с балансa.",
        'welcome_back': "🎉 Добро пожаловать! Ваши данные восстановлены.",
        'referral_info': "🔗 Ваша реферальная ссылка:\n{link}\n\n💰 Вы получаете +{reward} ⭐ за каждого пользователя!\n👥 Приглашено: {count}",
        'referral_bonus': "🎉 Вы получили +{stars} ⭐ за приглашение нового пользователя!",
        'welcome_bonus': "🎉 Добро пожаловать! Вы получили +{stars} ⭐ бонус за переход по ссылке!",
        'already_referred': "❌ Вас уже пригласил другой пользователь.",
        'premium_info': "💎 Преимущества Премиум:\n\n🔗 Рефералы: +7 ⭐ за пользователя (вместо +3)\n👤 Новые пользователи получают: +3 ⭐ (вместо +1)\n📝 Задания: +1 ⭐ за задание (вместо +0.40)\n\n⏰ Длительность: 30 дней\n💰 Цена: 100 Telegram Stars",
        'buy_premium': "💎 Купить Премиум",
        'premium_active': "✅ Премиум активен до: {date}",
        'premium_expired': "❌ Ваш премиум истёк",
        'slot_machine': "🎰 Игровой автомат",
        'fishing_game': "🎣 Рыбалка",
        'slot_bet': "🎰 Выберите ставку:",
        'slot_result_win': "🎉 ДЖЕКПОТ! 777\nВы выиграли {amount} ⭐!",
        'slot_result_lose': "😢 {result}\nВы проиграли {bet} ⭐",
        'fishing_choose': "🎣 Выберите способ рыбалки:",
        'fishing_garpoon': "🔱 Гарпун (Лучший)",
        'fishing_rod': "🎣 Удочка (Средний)",
        'fishing_hands': "✋ Руками (Слабый)",
        'fishing_cooldown': "⏰ Подождите {hours}ч {minutes}м до следующей рыбалки",
        'fishing_result': "🎣 Вы поймали {amount} ⭐ используя {method}!",
        'fishing_nothing': "😞 В этот раз ничего не поймали...",
        'insufficient_for_bet': "❌ Недостаточно звёзд для ставки. У вас {balance} ⭐",
        'farm_cooldown': "⏰ Подождите {hours}ч {minutes}м до следующего фарма",
        'farm_reward': "🎉 Вы нафармили {stars} ⭐ и получили +1 просмотр!\n\nТеперь выполните задание для подтверждения награды:",
        'farm_task_completed': "✅ Задание выполнено! Ваши {stars} ⭐ и просмотр подтверждены!"
    },
    'uk': {
        'welcome': "🎉 Ласкаво просимо! Оберіть вашу мову:",
        'language_changed': "✅ Мову змінено на українську",
        'main_menu': "☰ Головне меню",
        'menu_button': "☰ Меню",
        'balance': "📊 Баланс",
        'gift_shop': "🛍️ Магазин подарунків",
        'change_language': "🌐 Змінити мову",
        'tasks': "📝 Завдання",
        'restart_bot': "🔁 Перезапустити бота",
        'referral': "🔗 Реферальна система",
        'premium': "💎 Преміум",
        'mini_games': "🎮 Міні-ігри",
        'farm_stars': "🚀 Фарм зірок і переглядів",
        'bot_restarted': "✅ Бот успішно перезапущений.",
        'your_balance': "💰 Ваш баланс: {stars} ⭐\n👁️ Перегляди: {views}",
        'no_tasks': "✅ Немає доступних завдань",
        'task_subscribe': "📢 Підпишіться на канал: {channel}\n\nПісля підписки натисніть 'Готово'",
        'task_done': "✅ Готово",
        'task_completed': "🎉 Завдання виконано! +{reward} ⭐ додано",
        'task_not_subscribed': "❌ Ви не підписалися на канал. Нагорода не нарахована. Підпишіться, щоб отримати зірки.",
        'gift_heart': "❤️ Серце - 20 ⭐",
        'gift_box': "🎁 Коробка - 20 ⭐",
        'gift_rose': "🌹 Троянда - 100 ⭐",
        'gift_ring': "💍 Кільце - 100 ⭐",
        'insufficient_stars': "❌ Недостатньо зірок. Потрібно {needed} ⭐",
        'insufficient_requirements': "❌ Недостатньо вимог:\n• Реферали: {user_refs}/{req_refs}\n• Перегляди: {user_views}/{req_views}\n• Зірки: {user_stars}/{req_stars} ⭐",
        'gift_requested': "✅ Запит надіслано! Обробка протягом 1-2 днів",
        'admin_only': "❌ Тільки для адміністратора",
        'admin_help': "Команди адміністратора:\n/admin add <user_id> <amount> <reason>\n/admin remove <user_id> <amount> <reason>\n/admin ban <user_id> <reason>\n/admin stats",
        'user_not_found': "❌ Користувача не знайдено",
        'stars_added': "✅ {amount} ⭐ додано користувачу {user_id}",
        'stars_removed': "✅ {amount} ⭐ забрано у користувача {user_id}",
        'user_banned': "✅ Користувача {user_id} заблоковано",
        'you_are_banned': "❌ Вас заблоковано і ви не можете використовувати бота",
        'back': "⬅️ Назад",
        'unsubscribed_penalty': "❌ Ви відписалися від {channel} протягом 7 днів. {stars} ⭐ списано з балансу.",
        'welcome_back': "🎉 Ласкаво просимо! Ваші дані відновлено.",
        'referral_info': "🔗 Ваше реферальне посилання:\n{link}\n\n💰 Ви отримуєте +{reward} ⭐ за кожного користувача!\n👥 Запрошено: {count}",
        'referral_bonus': "🎉 Ви отримали +{stars} ⭐ за запрошення нового користувача!",
        'welcome_bonus': "🎉 Вітаємо! Ви отримали +{stars} ⭐ бонус за перехід по посиланню!",
        'already_referred': "❌ Вас вже запросив інший користувач.",
        'premium_info': "💎 Переваги Преміум:\n\n🔗 Реферали: +7 ⭐ за користувача (замість +3)\n👤 Нові користувачі отримують: +3 ⭐ (замість +1)\n📝 Завдання: +1 ⭐ за завдання (замість +0.40)\n\n⏰ Тривалість: 30 днів\n💰 Ціна: 100 Telegram Stars",
        'buy_premium': "💎 Купити Преміум",
        'premium_active': "✅ Преміум активний до: {date}",
        'premium_expired': "❌ Ваш преміум закінчився",
        'slot_machine': "🎰 Ігровий автомат",
        'fishing_game': "🎣 Риболовля",
        'slot_bet': "🎰 Оберіть ставку:",
        'slot_result_win': "🎉 ДЖЕКПОТ! 777\nВи виграли {amount} ⭐!",
        'slot_result_lose': "😢 {result}\nВи програли {bet} ⭐",
        'fishing_choose': "🎣 Оберіть спосіб риболовлі:",
        'fishing_garpoon': "🔱 Гарпун (Найкращий)",
        'fishing_rod': "🎣 Вудка (Середній)",
        'fishing_hands': "✋ Руками (Слабкий)",
        'fishing_cooldown': "⏰ Зачекайте {hours}г {minutes}хв до наступної риболовлі",
        'fishing_result': "🎣 Ви спіймали {amount} ⭐ використовуючи {method}!",
        'fishing_nothing': "😞 Цього разу нічого не спіймали...",
        'insufficient_for_bet': "❌ Недостатньо зірок для ставки. У вас {balance} ⭐",
        'farm_cooldown': "⏰ Зачекайте {hours}г {minutes}хв до наступного фарму",
        'farm_reward': "🎉 Ви нафармили {stars} ⭐ і отримали +1 перегляд!\n\nТепер виконайте завдання для підтвердження нагороди:",
        'farm_task_completed': "✅ Завдання виконано! Ваші {stars} ⭐ і перегляд підтверджені!"
    },
    'de': {
        'welcome': "🎉 Willkommen! Bitte wählen Sie Ihre Sprache:",
        'language_changed': "✅ Sprache auf Deutsch geändert",
        'main_menu': "☰ Hauptmenü",
        'menu_button': "☰ Menü",
        'balance': "📊 Guthaben",
        'gift_shop': "🛍️ Geschenkeladen",
        'change_language': "🌐 Sprache ändern",
        'tasks': "📝 Aufgaben",
        'restart_bot': "🔁 Bot neu starten",
        'referral': "🔗 Empfehlungssystem",
        'premium': "💎 Premium",
        'mini_games': "🎮 Mini-Spiele",
        'farm_stars': "🚀 Sterne & Aufrufe farmen",
        'bot_restarted': "✅ Bot erfolgreich neu gestartet.",
        'your_balance': "💰 Ihr Guthaben: {stars} ⭐\n👁️ Aufrufe: {views}",
        'no_tasks': "✅ Keine Aufgaben verfügbar",
        'task_subscribe': "📢 Abonnieren Sie diesen Kanal: {channel}\n\nNach dem Abonnieren drücken Sie 'Fertig'",
        'task_done': "✅ Fertig",
        'task_completed': "🎉 Aufgabe abgeschlossen! +{reward} ⭐ hinzugefügt",
        'task_not_subscribed': "❌ Sie haben den Kanal nicht abonniert. Ihre Belohnung wurde nicht gutgeschrieben. Bitte abonnieren Sie, um Ihre Sterne zu erhalten.",
        'gift_heart': "❤️ Herz - 20 ⭐",
        'gift_box': "🎁 Box - 20 ⭐",
        'gift_rose': "🌹 Rose - 100 ⭐",
        'gift_ring': "💍 Ring - 100 ⭐",
        'insufficient_stars': "❌ Nicht genug Sterne. Sie brauchen {needed} ⭐",
        'insufficient_requirements': "❌ Unzureichende Anforderungen:\n• Empfehlungen: {user_refs}/{req_refs}\n• Aufrufe: {user_views}/{req_views}\n• Sterne: {user_stars}/{req_stars} ⭐",
        'gift_requested': "✅ Geschenkanfrage gesendet! Bearbeitung in 1-2 Tagen",
        'admin_only': "❌ Nur für Administrator",
        'admin_help': "Admin-Befehle:\n/admin add <user_id> <amount> <reason>\n/admin remove <user_id> <amount> <reason>\n/admin ban <user_id> <reason>\n/admin stats",
        'user_not_found': "❌ Benutzer nicht gefunden",
        'stars_added': "✅ {amount} ⭐ zu Benutzer {user_id} hinzugefügt",
        'stars_removed': "✅ {amount} ⭐ von Benutzer {user_id} entfernt",
        'user_banned': "✅ Benutzer {user_id} wurde gesperrt",
        'you_are_banned': "❌ Sie wurden gesperrt und können den Bot nicht verwenden",
        'back': "⬅️ Zurück",
        'unsubscribed_penalty': "❌ Sie haben {channel} innerhalb von 7 Tagen deabonniert. {stars} ⭐ wurden entfernt.",
        'welcome_back': "🎉 Willkommen zurück! Ihre Daten wurden wiederhergestellt.",
        'referral_info': "🔗 Ihr Empfehlungslink:\n{link}\n\n💰 Sie erhalten +{reward} ⭐ für jeden Benutzer!\n👥 Empfohlen: {count}",
        'referral_bonus': "🎉 Sie haben +{stars} ⭐ für die Einladung eines neuen Benutzers erhalten!",
        'welcome_bonus': "🎉 Willkommen! Sie haben +{stars} ⭐ Bonus für den Beitritt über Empfehlung erhalten!",
        'already_referred': "❌ Sie wurden bereits von jemand anderem empfohlen.",
        'premium_info': "💎 Premium-Vorteile:\n\n🔗 Empfehlungen: +7 ⭐ pro Benutzer (statt +3)\n👤 Neue Benutzer erhalten: +3 ⭐ (statt +1)\n📝 Aufgaben: +1 ⭐ pro Aufgabe (statt +0.40)\n\n⏰ Dauer: 30 Tage\n💰 Preis: 100 Telegram Stars",
        'buy_premium': "💎 Premium kaufen",
        'premium_active': "✅ Premium ist aktiv bis: {date}",
        'premium_expired': "❌ Ihr Premium ist abgelaufen",
        'slot_machine': "🎰 Spielautomat",
        'fishing_game': "🎣 Angelspiel",
        'slot_bet': "🎰 Wählen Sie Ihren Einsatz:",
        'slot_result_win': "🎉 JACKPOT! 777\nSie haben {amount} ⭐ gewonnen!",
        'slot_result_lose': "😢 {result}\nSie haben {bet} ⭐ verloren",
        'fishing_choose': "🎣 Wählen Sie Ihre Angelmethode:",
        'fishing_garpoon': "🔱 Harpune (Beste)",
        'fishing_rod': "🎣 Angel (Mittel)",
        'fishing_hands': "✋ Bloße Hände (Niedrig)",
        'fishing_cooldown': "⏰ Sie müssen {hours}h {minutes}m warten, bevor Sie wieder angeln können",
        'fishing_result': "🎣 Sie haben {amount} ⭐ mit {method} gefangen!",
        'fishing_nothing': "😞 Diesmal haben Sie nichts gefangen...",
        'insufficient_for_bet': "❌ Nicht genug Sterne für diesen Einsatz. Sie haben {balance} ⭐",
        'farm_cooldown': "⏰ Sie müssen {hours}h {minutes}m warten, bevor Sie wieder farmen können",
        'farm_reward': "🎉 Sie haben {stars} ⭐ gefarmt und +1 Aufruf erhalten!\n\nJetzt schließen Sie diese Aufgabe ab, um Ihre Belohnung zu bestätigen:",
        'farm_task_completed': "✅ Aufgabe abgeschlossen! Ihre {stars} ⭐ und Ihr Aufruf wurden bestätigt!"
    }
}

# Gift prices
GIFTS = {
    'heart': {'price': 20, 'emoji': '❤️', 'name': 'Heart'},
    'box': {'price': 20, 'emoji': '🎁', 'name': 'Box'},
    'rose': {'price': 100, 'emoji': '🌹', 'name': 'Rose'},
    'ring': {'price': 100, 'emoji': '💍', 'name': 'Ring'}
}

# Slot machine bets
SLOT_BETS = [0.5, 1, 2, 5, 10, 20, 50, 100, 200, 300, 500, 1000]

# Farm tasks
FARM_TASKS = [
    "Join our main channel",
    "Subscribe to our updates",
    "Follow us on social media",
    "Share the bot with friends",
    "Rate us 5 stars",
    "Join our community chat",
    "Complete your profile"
]

# Your specific channels
CHANNELS = [
    'https://t.me/squeeze_svj',
    'https://t.me/sellnftgiftcepu',
    'https://t.me/+MbznMdNSxdJiZmNi',
    'https://t.me/+L6XvO_kn0cU4MmNh',
    'https://t.me/+ecS3oDBn_ZI4Mjdh',
    'https://t.me/+2rVxkmODXE9mMTU5',
    'https://t.me/+KJ3IrQQvrPUyOGZh'
]

# Data storage functions
def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            'users': {},
            'channels': CHANNELS,
            'subscriptions': {},
            'banned_users': []
        }

def save_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Error saving data: {e}")

def get_user_data(user_id, username=None):
    data = load_data()
    if str(user_id) not in data['users']:
        data['users'][str(user_id)] = {
            'language': 'en',
            'stars': 0.0,
            'views': 0,
            'subscriptions': {},
            'current_task': None,
            'username': username,
            'created_at': datetime.now().isoformat(),
            'referred_by': None,
            'referral_count': 0,
            'premium_until': None,
            'last_fishing': None,
            'last_farm': None,
            'pending_farm_reward': None,
            'gift_withdrawals': 0
        }
        save_data(data)
    elif username and data['users'][str(user_id)].get('username') != username:
        data['users'][str(user_id)]['username'] = username
        save_data(data)
    return data['users'][str(user_id)]

def update_user_data(user_id, user_data):
    data = load_data()
    data['users'][str(user_id)] = user_data
    save_data(data)

def is_user_banned(user_id):
    data = load_data()
    return str(user_id) in data.get('banned_users', [])

def ban_user(user_id):
    data = load_data()
    if 'banned_users' not in data:
        data['banned_users'] = []
    if str(user_id) not in data['banned_users']:
        data['banned_users'].append(str(user_id))
    save_data(data)

def is_premium(user_id):
    user_data = get_user_data(user_id)
    if not user_data.get('premium_until'):
        return False
    premium_until = datetime.fromisoformat(user_data['premium_until'])
    return datetime.now() < premium_until

def get_task_reward(user_id):
    return 1.0 if is_premium(user_id) else 0.4

def get_referral_reward(user_id):
    return 7 if is_premium(user_id) else 3

def get_welcome_bonus(user_id):
    return 3 if is_premium(user_id) else 1

def get_withdrawal_requirements(withdrawal_count):
    """Calculate referral and view requirements for gift withdrawal"""
    if withdrawal_count == 0:
        return {'referrals': 5, 'views': 10}
    elif withdrawal_count == 1:
        return {'referrals': 10, 'views': 20}
    else:
        # Each subsequent withdrawal requires +5 referrals and +10 views
        base_refs = 10 + (withdrawal_count - 1) * 5
        base_views = 20 + (withdrawal_count - 1) * 10
        return {'referrals': base_refs, 'views': base_views}

def get_text(user_id, key, **kwargs):
    user_data = get_user_data(user_id)
    lang = user_data.get('language', 'en')
    text = LANGUAGES[lang].get(key, LANGUAGES['en'][key])
    return text.format(**kwargs) if kwargs else text

def find_user_by_username_or_id(identifier):
    """Find user by username or user_id"""
    data = load_data()

    # Try to find by user_id first
    if identifier.isdigit():
        if identifier in data['users']:
            return identifier

    # Remove @ if present
    if identifier.startswith('@'):
        identifier = identifier[1:]

    # Search by username
    for user_id, user_data in data['users'].items():
        if user_data.get('username') == identifier:
            return user_id

    return None

async def check_channel_subscription(bot, user_id, channel_url):
    """Check if user is subscribed to a channel"""
    try:
        # Extract channel username from URL
        if channel_url.startswith('https://t.me/+'):
            # Private channel - can't check easily, assume subscribed for now
            return True
        elif channel_url.startswith('https://t.me/'):
            channel_username = '@' + channel_url.split('/')[-1]
        else:
            return False

        # Check membership
        member = await bot.get_chat_member(channel_username, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logger.error(f"Error checking subscription for {channel_url}: {e}")
        # If we can't check, assume user is subscribed to avoid false negatives
        return True

# Language selection
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        username = update.effective_user.username

        # Check if user is banned
        if is_user_banned(user_id):
            await update.message.reply_text(get_text(user_id, 'you_are_banned'))
            return

        # Handle referral
        referrer_id = None
        if context.args and context.args[0].startswith('ref_'):
            try:
                referrer_id = int(context.args[0].replace('ref_', ''))
            except ValueError:
                pass

        logger.info(f"User {user_id} started the bot")
        user_data = get_user_data(user_id, username)

        # Handle referral logic
        if referrer_id and referrer_id != user_id and not user_data.get('referred_by'):
            referrer_data = get_user_data(referrer_id)
            if referrer_data:
                # Give bonus to referrer
                referrer_reward = get_referral_reward(referrer_id)
                referrer_data['stars'] += referrer_reward
                referrer_data['referral_count'] = referrer_data.get('referral_count', 0) + 1
                update_user_data(referrer_id, referrer_data)

                # Give bonus to new user
                welcome_bonus = get_welcome_bonus(referrer_id)
                user_data['stars'] += welcome_bonus
                user_data['referred_by'] = referrer_id
                update_user_data(user_id, user_data)

                # Notify referrer
                try:
                    await context.bot.send_message(
                        chat_id=referrer_id,
                        text=get_text(referrer_id, 'referral_bonus', stars=referrer_reward)
                    )
                except:
                    pass

        # If user already has data, show welcome back message
        if user_data.get('language') and user_data.get('stars', 0) > 0:
            await show_main_menu(update, context)
        elif user_data.get('language'):
            await show_main_menu(update, context)
        else:
            keyboard = [
                [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")],
                [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
                [InlineKeyboardButton("🇺🇦 Українська", callback_data="lang_uk")],
                [InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_de")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "🎉 Welcome! Please choose your language:\n"
                "🎉 Добро пожаловать! Выберите ваш язык:\n"
                "🎉 Ласкаво просимо! Оберіть вашу мову:\n"
                "🎉 Willkommen! Bitte wählen Sie Ihre Sprache:",
                reply_markup=reply_markup
            )
    except Exception as e:
        logger.error(f"Error in start function: {e}")

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # Check if user is banned
    if is_user_banned(user_id):
        await query.edit_message_text(get_text(user_id, 'you_are_banned'))
        return

    lang = query.data.split('_')[1]

    user_data = get_user_data(user_id)
    user_data['language'] = lang
    update_user_data(user_id, user_data)

    # If called from the change language menu, go back to main menu
    if hasattr(query, 'message') and query.message.text and "Choose language:" in query.message.text:
        # Show the main menu in the new language
        await show_main_menu_message(query, context)
    else:
        # Initial language selection
        await query.edit_message_text(get_text(user_id, 'language_changed'))

        # Show the main keyboard with Menu button
        keyboard = [[KeyboardButton(get_text(user_id, 'menu_button'))]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        # Send a new message with the keyboard in the selected language
        await query.message.reply_text(
            get_text(user_id, 'welcome_back'),
            reply_markup=reply_markup
        )

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if user is banned
    if is_user_banned(user_id):
        await update.message.reply_text(get_text(user_id, 'you_are_banned'))
        return

    # Create simple keyboard with just Menu button
    keyboard = [[KeyboardButton(get_text(user_id, 'menu_button'))]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        get_text(user_id, 'welcome_back') if get_user_data(user_id).get('stars', 0) > 0 else "Welcome!",
        reply_markup=reply_markup
    )

async def show_main_menu_message(query, context: ContextTypes.DEFAULT_TYPE):
    user_id = query.from_user.id

    # Check if user is banned
    if is_user_banned(user_id):
        await query.message.reply_text(get_text(user_id, 'you_are_banned'))
        return

    keyboard = [
        [InlineKeyboardButton(get_text(user_id, 'balance'), callback_data="menu_balance"), 
         InlineKeyboardButton(get_text(user_id, 'tasks'), callback_data="menu_tasks")],
        [InlineKeyboardButton(get_text(user_id, 'farm_stars'), callback_data="menu_farm_stars"),
         InlineKeyboardButton(get_text(user_id, 'gift_shop'), callback_data="menu_gift_shop")],
        [InlineKeyboardButton(get_text(user_id, 'referral'), callback_data="menu_referral"),
         InlineKeyboardButton(get_text(user_id, 'premium'), callback_data="menu_premium")],
        [InlineKeyboardButton(get_text(user_id, 'mini_games'), callback_data="menu_mini_games")],
        [InlineKeyboardButton(get_text(user_id, 'change_language'), callback_data="menu_change_language")],
        [InlineKeyboardButton(get_text(user_id, 'restart_bot'), callback_data="menu_restart_bot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        get_text(user_id, 'main_menu'),
        reply_markup=reply_markup
    )

# Farm Stars & Views handler
async def show_farm_stars(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if user is banned
    if is_user_banned(user_id):
        await update.message.reply_text(get_text(user_id, 'you_are_banned'))
        return

    user_data = get_user_data(user_id)
    
    # Check cooldown (2 hours)
    if user_data.get('last_farm'):
        last_farm = datetime.fromisoformat(user_data['last_farm'])
        time_diff = datetime.now() - last_farm
        if time_diff < timedelta(hours=2):
            remaining = timedelta(hours=2) - time_diff
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            
            keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                get_text(user_id, 'farm_cooldown', hours=hours, minutes=minutes),
                reply_markup=reply_markup
            )
            return
    
    # Generate random star reward (0.1-3 stars)
    # Common: 0.1-2 stars (70% chance)
    # Rare: 2-3 stars (30% chance)
    if random.random() < 0.7:
        # Common drop
        stars_reward = round(random.uniform(0.1, 2.0), 1)
    else:
        # Rare drop
        stars_reward = round(random.uniform(2.0, 3.0), 1)
    
    # Set farm cooldown and store pending reward
    user_data['last_farm'] = datetime.now().isoformat()
    user_data['pending_farm_reward'] = {
        'stars': stars_reward,
        'views': 1,
        'task': random.choice(FARM_TASKS),
        'created_at': datetime.now().isoformat()
    }
    update_user_data(user_id, user_data)
    
    # Show task to complete
    keyboard = [
        [InlineKeyboardButton(get_text(user_id, 'task_done'), callback_data="farm_task_done")],
        [InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        get_text(user_id, 'farm_reward', stars=stars_reward) + f"\n\n📝 {user_data['pending_farm_reward']['task']}",
        reply_markup=reply_markup
    )

async def farm_task_done_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # Check if user is banned
    if is_user_banned(user_id):
        await query.edit_message_text(get_text(user_id, 'you_are_banned'))
        return

    user_data = get_user_data(user_id)
    
    if not user_data.get('pending_farm_reward'):
        await query.edit_message_text("❌ No pending farm reward found.")
        return
    
    reward = user_data['pending_farm_reward']
    
    # Add rewards
    user_data['stars'] += reward['stars']
    user_data['views'] += reward['views']
    user_data['pending_farm_reward'] = None
    update_user_data(user_id, user_data)
    
    keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        get_text(user_id, 'farm_task_completed', stars=reward['stars']),
        reply_markup=reply_markup
    )

async def admin_task_done_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # Check if user is banned
    if is_user_banned(user_id):
        await query.edit_message_text(get_text(user_id, 'you_are_banned'))
        return

    task_id = query.data.split('_', 3)[3]
    user_data = get_user_data(user_id)
    data = load_data()
    
    # Find the admin task
    admin_tasks = data.get('admin_tasks', [])
    task = next((t for t in admin_tasks if t['id'] == task_id), None)
    
    if not task:
        await query.edit_message_text("❌ Task not found.")
        return
    
    # Check if user already completed this task
    if 'completed_admin_tasks' not in user_data:
        user_data['completed_admin_tasks'] = []
    
    if task_id in user_data['completed_admin_tasks']:
        await query.edit_message_text("❌ You have already completed this task.")
        return
    
    # For now, we'll assume the user completed the task (manual verification)
    # In a real implementation, you could add verification logic here
    
    # Add reward and mark as completed
    user_data['stars'] += task['reward']
    user_data['completed_admin_tasks'].append(task_id)
    user_data['current_task'] = None
    
    # Add user to task completion list
    if task_id not in [t['id'] for t in admin_tasks if user_id in t.get('completed_by', [])]:
        task['completed_by'].append(user_id)
        save_data(data)
    
    update_user_data(user_id, user_data)
    
    # Notify admin about completion
    try:
        username = query.from_user.username or f"ID{user_id}"
        if username != f"ID{user_id}":
            username = f"@{username}"
        
        notification_text = (
            f"✅ Task completed!\n\n"
            f"👤 User: {username}\n"
            f"📝 Task: {task['description']}\n"
            f"⭐ Reward: {task['reward']} stars\n"
            f"🔗 Link: {task['link']}"
        )
        
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=notification_text
        )
    except Exception as e:
        logger.error(f"Failed to notify admin: {e}")
    
    keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"🎉 Task completed! +{task['reward']} ⭐ added to your balance\n\n📝 {task['description']}",
        reply_markup=reply_markup
    )

# Balance handler
async def show_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if user is banned
    if is_user_banned(user_id):
        await update.message.reply_text(get_text(user_id, 'you_are_banned'))
        return

    user_data = get_user_data(user_id)
    stars = user_data.get('stars', 0)
    views = user_data.get('views', 0)
    invited_users = user_data.get('referral_count', 0)

    keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    balance_text = get_text(user_id, 'your_balance', stars=stars, views=views) + f"\n🔗 Invited users: {invited_users}"

    await update.message.reply_text(
        balance_text,
        reply_markup=reply_markup
    )

# Tasks handler
async def show_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if user is banned
    if is_user_banned(user_id):
        await update.message.reply_text(get_text(user_id, 'you_are_banned'))
        return

    user_data = get_user_data(user_id)
    data = load_data()

    # Check if user has a current task
    if user_data.get('current_task'):
        if user_data['current_task'].startswith('admin_task_'):
            # Handle admin task
            task_id = user_data['current_task']
            admin_tasks = data.get('admin_tasks', [])
            task = next((t for t in admin_tasks if t['id'] == task_id), None)
            
            if task:
                keyboard = [
                    [InlineKeyboardButton(get_text(user_id, 'task_done'), callback_data=f"admin_task_done_{task_id}")],
                    [InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text(
                    f"📝 {task['description']}\n⭐ Reward: {task['reward']} stars\n\n🔗 Link: {task['link']}\n\nComplete this task and press 'Done'",
                    reply_markup=reply_markup
                )
            else:
                user_data['current_task'] = None
                update_user_data(user_id, user_data)
                await show_tasks(update, context)
        else:
            # Handle channel subscription task
            channel = user_data['current_task']
            keyboard = [
                [InlineKeyboardButton(get_text(user_id, 'task_done'), callback_data=f"task_done_{channel}")],
                [InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                get_text(user_id, 'task_subscribe', channel=channel),
                reply_markup=reply_markup
            )
    else:
        # First check for available admin tasks
        admin_tasks = data.get('admin_tasks', [])
        completed_admin_tasks = user_data.get('completed_admin_tasks', [])
        available_admin_tasks = [t for t in admin_tasks if t['id'] not in completed_admin_tasks]
        
        if available_admin_tasks:
            # Assign first available admin task
            task = available_admin_tasks[0]
            user_data['current_task'] = task['id']
            update_user_data(user_id, user_data)
            
            keyboard = [
                [InlineKeyboardButton(get_text(user_id, 'task_done'), callback_data=f"admin_task_done_{task['id']}")],
                [InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                f"📝 {task['description']}\n⭐ Reward: {task['reward']} stars\n\n🔗 Link: {task['link']}\n\nComplete this task and press 'Done'",
                reply_markup=reply_markup
            )
        else:
            # Then check for channel subscription tasks
            channels = data.get('channels', CHANNELS)
            completed_channels = list(user_data.get('subscriptions', {}).keys())
            available_channels = [ch for ch in channels if ch not in completed_channels]

            if available_channels:
                channel = available_channels[0]
                user_data['current_task'] = channel
                update_user_data(user_id, user_data)

                keyboard = [
                    [InlineKeyboardButton(get_text(user_id, 'task_done'), callback_data=f"task_done_{channel}")],
                    [InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text(
                    get_text(user_id, 'task_subscribe', channel=channel),
                    reply_markup=reply_markup
                )
            else:
                keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text(
                    get_text(user_id, 'no_tasks'),
                    reply_markup=reply_markup
                )

async def task_done_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # Check if user is banned
    if is_user_banned(user_id):
        await query.edit_message_text(get_text(user_id, 'you_are_banned'))
        return

    channel = query.data.split('_', 2)[2]
    user_data = get_user_data(user_id)

    # Check if user is actually subscribed to the channel
    is_subscribed = await check_channel_subscription(context.bot, user_id, channel)

    if not is_subscribed:
        await query.edit_message_text(get_text(user_id, 'task_not_subscribed'))
        return

    # Add stars and record subscription
    reward = get_task_reward(user_id)
    user_data['stars'] = user_data.get('stars', 0) + reward
    user_data['subscriptions'][channel] = {
        'subscribed_at': datetime.now().isoformat(),
        'stars_given': reward
    }
    user_data['current_task'] = None
    update_user_data(user_id, user_data)

    await query.edit_message_text(get_text(user_id, 'task_completed', reward=reward))

# Referral handler
async def show_referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if user is banned
    if is_user_banned(user_id):
        await update.message.reply_text(get_text(user_id, 'you_are_banned'))
        return

    user_data = get_user_data(user_id)
    bot_username = context.bot.username
    referral_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    referral_count = user_data.get('referral_count', 0)
    reward = get_referral_reward(user_id)

    keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        get_text(user_id, 'referral_info', link=referral_link, reward=reward, count=referral_count),
        reply_markup=reply_markup
    )

# Premium handler
async def show_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if user is banned
    if is_user_banned(user_id):
        await update.message.reply_text(get_text(user_id, 'you_are_banned'))
        return

    user_data = get_user_data(user_id)
    
    if is_premium(user_id):
        premium_until = datetime.fromisoformat(user_data['premium_until'])
        keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            get_text(user_id, 'premium_active', date=premium_until.strftime('%Y-%m-%d %H:%M')),
            reply_markup=reply_markup
        )
    else:
        keyboard = [
            [InlineKeyboardButton(get_text(user_id, 'buy_premium'), callback_data="buy_premium")],
            [InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            get_text(user_id, 'premium_info'),
            reply_markup=reply_markup
        )

# Mini-games handler
async def show_mini_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if user is banned
    if is_user_banned(user_id):
        await update.message.reply_text(get_text(user_id, 'you_are_banned'))
        return

    keyboard = [
        [InlineKeyboardButton(get_text(user_id, 'slot_machine'), callback_data="game_slots"),
         InlineKeyboardButton(get_text(user_id, 'fishing_game'), callback_data="game_fishing")],
        [InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        get_text(user_id, 'mini_games'),
        reply_markup=reply_markup
    )

# Slot machine game
async def show_slot_machine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    keyboard = []
    for i in range(0, len(SLOT_BETS), 3):
        row = []
        for j in range(3):
            if i + j < len(SLOT_BETS):
                bet = SLOT_BETS[i + j]
                row.append(InlineKeyboardButton(f"{bet} ⭐", callback_data=f"slot_bet_{bet}"))
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton(get_text(user_id, 'back'), callback_data="menu_mini_games")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        get_text(user_id, 'slot_bet'),
        reply_markup=reply_markup
    )

async def play_slots(query, bet_amount):
    user_id = query.from_user.id
    user_data = get_user_data(user_id)
    
    if user_data.get('stars', 0) < bet_amount:
        await query.edit_message_text(
            get_text(user_id, 'insufficient_for_bet', balance=user_data.get('stars', 0))
        )
        return
    
    # Generate slot result
    symbols = ['🍒', '🍋', '🍊', '🍇', '⭐', '💎', '7️⃣']
    result = [random.choice(symbols) for _ in range(3)]
    
    # Check for win (10% chance for 777, lower for other combinations)
    is_jackpot = random.random() < 0.1
    
    if is_jackpot:
        result = ['7️⃣', '7️⃣', '7️⃣']
        win_amount = bet_amount * 2
        user_data['stars'] += win_amount
        update_user_data(user_id, user_data)
        
        keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data="game_slots")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            get_text(user_id, 'slot_result_win', amount=win_amount),
            reply_markup=reply_markup
        )
    else:
        user_data['stars'] -= bet_amount
        update_user_data(user_id, user_data)
        
        keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data="game_slots")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        result_str = ''.join(result)
        await query.edit_message_text(
            get_text(user_id, 'slot_result_lose', result=result_str, bet=bet_amount),
            reply_markup=reply_markup
        )

# Fishing game
async def show_fishing_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data = get_user_data(user_id)
    
    # Check cooldown
    if user_data.get('last_fishing'):
        last_fishing = datetime.fromisoformat(user_data['last_fishing'])
        time_diff = datetime.now() - last_fishing
        if time_diff < timedelta(hours=12):
            remaining = timedelta(hours=12) - time_diff
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            
            keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data="menu_mini_games")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                get_text(user_id, 'fishing_cooldown', hours=hours, minutes=minutes),
                reply_markup=reply_markup
            )
            return
    
    keyboard = [
        [InlineKeyboardButton(get_text(user_id, 'fishing_garpoon'), callback_data="fish_garpoon")],
        [InlineKeyboardButton(get_text(user_id, 'fishing_rod'), callback_data="fish_rod")],
        [InlineKeyboardButton(get_text(user_id, 'fishing_hands'), callback_data="fish_hands")],
        [InlineKeyboardButton(get_text(user_id, 'back'), callback_data="menu_mini_games")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        get_text(user_id, 'fishing_choose'),
        reply_markup=reply_markup
    )

async def play_fishing(query, method):
    user_id = query.from_user.id
    user_data = get_user_data(user_id)
    
    # Set fishing cooldown
    user_data['last_fishing'] = datetime.now().isoformat()
    
    # Determine catch based on method
    if method == 'garpoon':
        success_rate = 0.8
        min_catch, max_catch = 0.5, 5.0
        method_name = get_text(user_id, 'fishing_garpoon').split(' ')[1]  # Remove emoji
    elif method == 'rod':
        success_rate = 0.6
        min_catch, max_catch = 0.5, 3.0
        method_name = get_text(user_id, 'fishing_rod').split(' ')[1]
    else:  # hands
        success_rate = 0.4
        min_catch, max_catch = 0.5, 2.0
        method_name = get_text(user_id, 'fishing_hands').split(' ')[2]
    
    if random.random() < success_rate:
        # Successful catch
        if is_premium(user_id):
            # Premium users get better rewards
            min_catch = max(min_catch, 1.0)
            max_catch += 1.0
        
        catch_amount = round(random.uniform(min_catch, max_catch), 1)
        user_data['stars'] += catch_amount
        update_user_data(user_id, user_data)
        
        keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data="menu_mini_games")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            get_text(user_id, 'fishing_result', amount=catch_amount, method=method_name),
            reply_markup=reply_markup
        )
    else:
        # No catch
        update_user_data(user_id, user_data)
        
        keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data="menu_mini_games")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            get_text(user_id, 'fishing_nothing'),
            reply_markup=reply_markup
        )

# Gift shop handler with new requirements
async def show_gift_shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if user is banned
    if is_user_banned(user_id):
        await update.message.reply_text(get_text(user_id, 'you_are_banned'))
        return

    # Create keyboard with 2 buttons per row
    keyboard = [
        [
            InlineKeyboardButton(get_text(user_id, 'gift_heart'), callback_data="gift_heart"),
            InlineKeyboardButton(get_text(user_id, 'gift_box'), callback_data="gift_box")
        ],
        [
            InlineKeyboardButton(get_text(user_id, 'gift_rose'), callback_data="gift_rose"),
            InlineKeyboardButton(get_text(user_id, 'gift_ring'), callback_data="gift_ring")
        ],
        [InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        get_text(user_id, 'gift_shop'),
        reply_markup=reply_markup
    )

async def gift_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # Check if user is banned
    if is_user_banned(user_id):
        await query.edit_message_text(get_text(user_id, 'you_are_banned'))
        return

    gift_id = query.data.split('_')[1]
    user_data = get_user_data(user_id)

    gift_info = GIFTS[gift_id]
    user_stars = user_data.get('stars', 0)
    user_refs = user_data.get('referral_count', 0)
    user_views = user_data.get('views', 0)
    withdrawal_count = user_data.get('gift_withdrawals', 0)
    
    # Get requirements for this withdrawal
    requirements = get_withdrawal_requirements(withdrawal_count)
    req_refs = requirements['referrals']
    req_views = requirements['views']
    req_stars = gift_info['price']
    
    # Check all requirements
    if user_stars >= req_stars and user_refs >= req_refs and user_views >= req_views:
        user_data['stars'] -= req_stars
        user_data['gift_withdrawals'] = withdrawal_count + 1
        update_user_data(user_id, user_data)

        # Send notification to your notification group
        try:
            username = query.from_user.username or f"ID{user_id}"
            if username != f"ID{user_id}":
                username = f"@{username}"

            notification_text = (
                f"{username} bought {gift_info['emoji']} for {gift_info['price']} stars!\n"
                f"Withdrawal #{withdrawal_count + 1}"
            )

            # Send to notification chat
            await context.bot.send_message(
                chat_id=NOTIFICATION_CHAT,
                text=notification_text
            )
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")

        await query.edit_message_text(get_text(user_id, 'gift_requested'))
    else:
        await query.edit_message_text(
            get_text(user_id, 'insufficient_requirements', 
                    user_refs=user_refs, req_refs=req_refs,
                    user_views=user_views, req_views=req_views,
                    user_stars=user_stars, req_stars=req_stars)
        )

# Language change handler
async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if user is banned
    if is_user_banned(user_id):
        await update.message.reply_text(get_text(user_id, 'you_are_banned'))
        return

    keyboard = [
        [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"), InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("🇺🇦 Українська", callback_data="lang_uk"), InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_de")],
        [InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(get_text(user_id, 'change_language'), reply_markup=reply_markup)

# Menu command handler
async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Check if user is banned
    if is_user_banned(user_id):
        await update.message.reply_text(get_text(user_id, 'you_are_banned'))
        return

    keyboard = [
        [InlineKeyboardButton(get_text(user_id, 'balance'), callback_data="menu_balance"), 
         InlineKeyboardButton(get_text(user_id, 'tasks'), callback_data="menu_tasks")],
        [InlineKeyboardButton(get_text(user_id, 'farm_stars'), callback_data="menu_farm_stars"),
         InlineKeyboardButton(get_text(user_id, 'gift_shop'), callback_data="menu_gift_shop")],
        [InlineKeyboardButton(get_text(user_id, 'referral'), callback_data="menu_referral"),
         InlineKeyboardButton(get_text(user_id, 'premium'), callback_data="menu_premium")],
        [InlineKeyboardButton(get_text(user_id, 'mini_games'), callback_data="menu_mini_games")],
        [InlineKeyboardButton(get_text(user_id, 'change_language'), callback_data="menu_change_language")],
        [InlineKeyboardButton(get_text(user_id, 'restart_bot'), callback_data="menu_restart_bot")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        get_text(user_id, 'main_menu'),
        reply_markup=reply_markup
    )

# Premium purchase handler with Telegram Stars payment
async def buy_premium_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    # Create Telegram Stars invoice
    try:
        title = "Premium Subscription"
        description = "30 days of Premium benefits:\n• +7 ⭐ per referral\n• +3 ⭐ for new users\n• +1 ⭐ per task"
        payload = f"premium_{user_id}_{datetime.now().timestamp()}"
        currency = "XTR"  # Telegram Stars currency
        prices = [LabeledPrice("Premium", 100)]  # 100 Telegram Stars
        
        # Send invoice
        await context.bot.send_invoice(
            chat_id=user_id,
            title=title,
            description=description,
            payload=payload,
            provider_token="",  # Empty for Telegram Stars
            currency=currency,
            prices=prices,
            start_parameter="premium_purchase",
            photo_url="https://telegra.ph/file/f3a4e1e6c8c4e5b6c7d8e.png",  # Optional premium icon
            photo_size=512,
            photo_width=512,
            photo_height=512,
            need_name=False,
            need_phone_number=False,
            need_email=False,
            need_shipping_address=False,
            send_phone_number_to_provider=False,
            send_email_to_provider=False,
            is_flexible=False
        )
        
        keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data="menu_premium")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "💎 Premium purchase invoice sent!\n\nPlease complete the payment using your Telegram Stars balance.",
            reply_markup=reply_markup
        )
        
    except Exception as e:
        logger.error(f"Error creating premium invoice: {e}")
        keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data="menu_premium")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "❌ Error creating payment invoice. Please try again later.",
            reply_markup=reply_markup
        )

# Handle successful payments
async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle successful Telegram Stars payments"""
    user_id = update.effective_user.id
    payment = update.message.successful_payment
    
    # Verify this is a premium purchase
    if payment.invoice_payload.startswith('premium_'):
        user_data = get_user_data(user_id)
        
        # Activate premium for 30 days
        premium_until = datetime.now() + timedelta(days=30)
        user_data['premium_until'] = premium_until.isoformat()
        update_user_data(user_id, user_data)
        
        # Send confirmation
        await update.message.reply_text(
            f"✅ Premium activated until: {premium_until.strftime('%d.%m.%Y')}\n\n"
            f"🎉 Thank you for your purchase! Your Premium benefits are now active."
        )
        
        # Log the purchase
        logger.info(f"Premium purchased by user {user_id} for {payment.total_amount} Telegram Stars")

# Pre-checkout query handler
async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Answer pre-checkout query"""
    query = update.pre_checkout_query
    
    # Verify the payload is valid
    if query.invoice_payload.startswith('premium_'):
        await query.answer(ok=True)
    else:
        await query.answer(ok=False, error_message="Invalid purchase request")

# Enhanced admin commands
async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        await update.message.reply_text(get_text(user_id, 'admin_only'))
        return

    if not context.args:
        await update.message.reply_text(get_text(user_id, 'admin_help'))
        return

    command = context.args[0].lower()

    try:
        if command == "add" and len(context.args) >= 4:
            target_identifier = context.args[1]
            amount_str = context.args[2].replace(',', '.')  # Handle both comma and dot decimals
            try:
                amount = float(amount_str)
            except ValueError:
                await update.message.reply_text("❌ Invalid amount. Please use a number (e.g., 2.5 or 0.4)")
                return
            reason = " ".join(context.args[3:])

            # Remove @ if present
            if target_identifier.startswith('@'):
                target_identifier = target_identifier[1:]

            target_user_id = find_user_by_username_or_id(target_identifier)

            if target_user_id:
                data = load_data()
                if target_user_id not in data['users']:
                    data['users'][target_user_id] = {
                        'language': 'en',
                        'stars': 0.0,
                        'views': 0,
                        'subscriptions': {},
                        'current_task': None,
                        'username': None,
                        'created_at': datetime.now().isoformat(),
                        'referred_by': None,
                        'referral_count': 0,
                        'premium_until': None,
                        'last_fishing': None,
                        'last_farm': None,
                        'pending_farm_reward': None,
                        'gift_withdrawals': 0
                    }
                data['users'][target_user_id]['stars'] += amount
                save_data(data)
                
                # Get username for display
                username = data['users'][target_user_id].get('username', f"ID{target_user_id}")
                
                await update.message.reply_text(
                    f"✅ Added {amount} ⭐ to user @{username} (ID: {target_user_id})\nReason: {reason}"
                )
                
                # Notify the user
                try:
                    await context.bot.send_message(
                        chat_id=int(target_user_id),
                        text=f"🎉 Admin added {amount} ⭐ to your balance!\nReason: {reason}"
                    )
                except:
                    pass
            else:
                await update.message.reply_text(f"❌ User @{target_identifier} not found")

        elif command == "remove" and len(context.args) >= 4:
            target_identifier = context.args[1]
            amount_str = context.args[2].replace(',', '.')  # Handle both comma and dot decimals
            try:
                amount = float(amount_str)
            except ValueError:
                await update.message.reply_text("❌ Invalid amount. Please use a number (e.g., 2.5 or 0.4)")
                return
            reason = " ".join(context.args[3:])

            # Remove @ if present
            if target_identifier.startswith('@'):
                target_identifier = target_identifier[1:]

            target_user_id = find_user_by_username_or_id(target_identifier)

            if target_user_id:
                data = load_data()
                if target_user_id in data['users']:
                    old_balance = data['users'][target_user_id]['stars']
                    data['users'][target_user_id]['stars'] = max(0, old_balance - amount)
                    save_data(data)
                    
                    # Get username for display
                    username = data['users'][target_user_id].get('username', f"ID{target_user_id}")
                    
                    await update.message.reply_text(
                        f"✅ Removed {amount} ⭐ from user @{username} (ID: {target_user_id})\nReason: {reason}\nOld balance: {old_balance} → New balance: {data['users'][target_user_id]['stars']}"
                    )
                    
                    # Notify the user
                    try:
                        await context.bot.send_message(
                            chat_id=int(target_user_id),
                            text=f"⚠️ Admin removed {amount} ⭐ from your balance.\nReason: {reason}"
                        )
                    except:
                        pass
                else:
                    await update.message.reply_text("❌ User not found in database")
            else:
                await update.message.reply_text(f"❌ User @{target_identifier} not found")

        elif command == "ban" and len(context.args) >= 3:
            target_identifier = context.args[1]
            reason = " ".join(context.args[2:])

            target_user_id = find_user_by_username_or_id(target_identifier)

            if target_user_id:
                ban_user(target_user_id)
                await update.message.reply_text(
                    f"✅ User {target_identifier} (ID: {target_user_id}) has been banned\nReason: {reason}"
                )

                # Try to notify the banned user
                try:
                    await context.bot.send_message(
                        chat_id=int(target_user_id),
                        text=get_text(int(target_user_id), 'you_are_banned')
                    )
                except Exception as e:
                    logger.error(f"Could not notify banned user {target_user_id}: {e}")
            else:
                await update.message.reply_text("❌ User not found")

        elif command == "new" and len(context.args) >= 4:
            # Admin new <reward_stars> <task_description> <verification_link>
            try:
                reward_stars = float(context.args[1].replace(',', '.'))
            except ValueError:
                await update.message.reply_text("❌ Invalid star amount. Please use a number (e.g., 2.5)")
                return
            
            task_description = " ".join(context.args[2:-1])
            verification_link = context.args[-1]
            
            # Store the new admin task
            data = load_data()
            if 'admin_tasks' not in data:
                data['admin_tasks'] = []
            
            task_id = f"admin_task_{len(data['admin_tasks']) + 1}_{int(datetime.now().timestamp())}"
            new_task = {
                'id': task_id,
                'description': task_description,
                'reward': reward_stars,
                'link': verification_link,
                'created_at': datetime.now().isoformat(),
                'completed_by': []
            }
            
            data['admin_tasks'].append(new_task)
            save_data(data)
            
            await update.message.reply_text(
                f"✅ New task created!\n\n"
                f"📝 Task: {task_description}\n"
                f"⭐ Reward: {reward_stars} stars\n"
                f"🔗 Link: {verification_link}\n"
                f"🆔 Task ID: {task_id}\n\n"
                f"Users can now complete this task through the Tasks menu."
            )

        elif command == "stats":
            data = load_data()
            users_count = len(data['users'])
            banned_count = len(data.get('banned_users', []))
            total_stars = sum(user.get('stars', 0) for user in data['users'].values())
            total_views = sum(user.get('views', 0) for user in data['users'].values())
            active_users = len([u for u in data['users'].values() if u.get('stars', 0) > 0])
            premium_users = len([u for u in data['users'].values() if u.get('premium_until') and datetime.now() < datetime.fromisoformat(u['premium_until'])])
            total_referrals = sum(user.get('referral_count', 0) for user in data['users'].values())
            admin_tasks = len(data.get('admin_tasks', []))

            stats_text = (
                f"📊 Bot Statistics:\n"
                f"👥 Total users: {users_count}\n"
                f"⭐ Total stars distributed: {total_stars:.1f}\n"
                f"👁️ Total views: {total_views}\n"
                f"✅ Active users (with stars): {active_users}\n"
                f"💎 Premium users: {premium_users}\n"
                f"🔗 Total referrals: {total_referrals}\n"
                f"📝 Admin tasks: {admin_tasks}\n"
                f"🚫 Banned users: {banned_count}"
            )
            await update.message.reply_text(stats_text)

        else:
            await update.message.reply_text(get_text(user_id, 'admin_help'))

    except Exception as e:
        logger.error(f"Error in admin command: {e}")
        await update.message.reply_text(f"❌ Error executing command: {str(e)}")

# Function to check if user is still subscribed to channels
async def check_subscriptions(context: ContextTypes.DEFAULT_TYPE):
    """Check for users who unsubscribed within 7 days and remove their stars"""
    try:
        data = load_data()
        bot = context.bot
        current_time = datetime.now()

        for user_id, user_data in data['users'].items():
            # Skip banned users
            if str(user_id) in data.get('banned_users', []):
                continue

            subscriptions = user_data.get('subscriptions', {})

            for channel, sub_info in list(subscriptions.items()):
                try:
                    subscribed_at = datetime.fromisoformat(sub_info['subscribed_at'])
                    days_since_subscription = (current_time - subscribed_at).days

                    # Only check subscriptions within 7 days
                    if days_since_subscription <= 7:
                        # Check if user is still subscribed
                        is_subscribed = await check_channel_subscription(bot, int(user_id), channel)

                        if not is_subscribed:
                            # User left within 7 days, remove stars
                            stars_to_remove = sub_info.get('stars_given', 0.4)
                            user_data['stars'] = max(0, user_data['stars'] - stars_to_remove)
                            del user_data['subscriptions'][channel]

                            # Notify user about star removal
                            try:
                                await bot.send_message(
                                    chat_id=int(user_id),
                                    text=get_text(int(user_id), 'unsubscribed_penalty', 
                                                 channel=channel, stars=stars_to_remove)
                                )
                            except:
                                pass  # User might have blocked the bot

                except Exception as e:
                    logger.error(f"Error checking subscription for user {user_id} in channel {channel}: {e}")
                    continue

        save_data(data)

    except Exception as e:
        logger.error(f"Error in check_subscriptions: {e}")

# Callback query handler for inline menu buttons
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    # Check if user is banned
    if is_user_banned(user_id):
        await query.answer()
        await query.edit_message_text(get_text(user_id, 'you_are_banned'))
        return

    data = query.data
    await query.answer()

    try:
        if data.startswith('lang_'):
            await language_callback(update, context)
        elif data.startswith('task_done_'):
            await task_done_callback(update, context)
        elif data.startswith('gift_'):
            await gift_callback(update, context)
        elif data.startswith('slot_bet_'):
            bet_amount = float(data.split('_')[2])
            await play_slots(query, bet_amount)
        elif data.startswith('fish_'):
            method = data.split('_')[1]
            await play_fishing(query, method)
        elif data == 'farm_task_done':
            await farm_task_done_callback(update, context)
        elif data.startswith('admin_task_done_'):
            await admin_task_done_callback(update, context)
        elif data == 'buy_premium':
            await buy_premium_callback(update, context)
        elif data == 'back_menu':
            await show_main_menu_message(query, context)
        elif data == 'menu_balance':
            user_data = get_user_data(user_id)
            stars = user_data.get('stars', 0)
            views = user_data.get('views', 0)
            invited_users = user_data.get('referral_count', 0)
            keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            balance_text = get_text(user_id, 'your_balance', stars=stars, views=views) + f"\n🔗 Invited users: {invited_users}"
            
            await query.edit_message_text(
                balance_text,
                reply_markup=reply_markup
            )
        elif data == 'menu_farm_stars':
            await handle_farm_stars_callback(query, context)
        elif data == 'menu_tasks':
            await handle_tasks_callback(query, context)
        elif data == 'menu_gift_shop':
            keyboard = [
                [
                    InlineKeyboardButton(get_text(user_id, 'gift_heart'), callback_data="gift_heart"),
                    InlineKeyboardButton(get_text(user_id, 'gift_box'), callback_data="gift_box")
                ],
                [
                    InlineKeyboardButton(get_text(user_id, 'gift_rose'), callback_data="gift_rose"),
                    InlineKeyboardButton(get_text(user_id, 'gift_ring'), callback_data="gift_ring")
                ],
                [InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                get_text(user_id, 'gift_shop'),
                reply_markup=reply_markup
            )
        elif data == 'menu_referral':
            user_data = get_user_data(user_id)
            bot_username = context.bot.username
            referral_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
            referral_count = user_data.get('referral_count', 0)
            reward = get_referral_reward(user_id)

            keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                get_text(user_id, 'referral_info', link=referral_link, reward=reward, count=referral_count),
                reply_markup=reply_markup
            )
        elif data == 'menu_premium':
            user_data = get_user_data(user_id)
            
            if is_premium(user_id):
                premium_until = datetime.fromisoformat(user_data['premium_until'])
                keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(
                    get_text(user_id, 'premium_active', date=premium_until.strftime('%Y-%m-%d %H:%M')),
                    reply_markup=reply_markup
                )
            else:
                keyboard = [
                    [InlineKeyboardButton(get_text(user_id, 'buy_premium'), callback_data="buy_premium")],
                    [InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(
                    get_text(user_id, 'premium_info'),
                    reply_markup=reply_markup
                )
        elif data == 'menu_mini_games':
            keyboard = [
                [InlineKeyboardButton(get_text(user_id, 'slot_machine'), callback_data="game_slots"),
                 InlineKeyboardButton(get_text(user_id, 'fishing_game'), callback_data="game_fishing")],
                [InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                get_text(user_id, 'mini_games'),
                reply_markup=reply_markup
            )
        elif data == 'game_slots':
            keyboard = []
            for i in range(0, len(SLOT_BETS), 3):
                row = []
                for j in range(3):
                    if i + j < len(SLOT_BETS):
                        bet = SLOT_BETS[i + j]
                        row.append(InlineKeyboardButton(f"{bet} ⭐", callback_data=f"slot_bet_{bet}"))
                keyboard.append(row)
            
            keyboard.append([InlineKeyboardButton(get_text(user_id, 'back'), callback_data="menu_mini_games")])
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                get_text(user_id, 'slot_bet'),
                reply_markup=reply_markup
            )
        elif data == 'game_fishing':
            user_data = get_user_data(user_id)
            
            # Check cooldown
            if user_data.get('last_fishing'):
                last_fishing = datetime.fromisoformat(user_data['last_fishing'])
                time_diff = datetime.now() - last_fishing
                if time_diff < timedelta(hours=12):
                    remaining = timedelta(hours=12) - time_diff
                    hours = remaining.seconds // 3600
                    minutes = (remaining.seconds % 3600) // 60
                    
                    keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data="menu_mini_games")]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    
                    await query.edit_message_text(
                        get_text(user_id, 'fishing_cooldown', hours=hours, minutes=minutes),
                        reply_markup=reply_markup
                    )
                    return
            
            keyboard = [
                [InlineKeyboardButton(get_text(user_id, 'fishing_garpoon'), callback_data="fish_garpoon")],
                [InlineKeyboardButton(get_text(user_id, 'fishing_rod'), callback_data="fish_rod")],
                [InlineKeyboardButton(get_text(user_id, 'fishing_hands'), callback_data="fish_hands")],
                [InlineKeyboardButton(get_text(user_id, 'back'), callback_data="menu_mini_games")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                get_text(user_id, 'fishing_choose'),
                reply_markup=reply_markup
            )
        elif data == 'menu_change_language':
            keyboard = [
                [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"), InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
                [InlineKeyboardButton("🇺🇦 Українська", callback_data="lang_uk"), InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_de")],
                [InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(get_text(user_id, 'change_language'), reply_markup=reply_markup)
        elif data == 'menu_restart_bot':
            keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                get_text(user_id, 'bot_restarted'),
                reply_markup=reply_markup
            )
    except Exception as e:
        logger.error(f"Error in callback handler: {e}")

async def handle_farm_stars_callback(query, context: ContextTypes.DEFAULT_TYPE):
    user_id = query.from_user.id
    user_data = get_user_data(user_id)
    
    # Check cooldown (2 hours)
    if user_data.get('last_farm'):
        last_farm = datetime.fromisoformat(user_data['last_farm'])
        time_diff = datetime.now() - last_farm
        if time_diff < timedelta(hours=2):
            remaining = timedelta(hours=2) - time_diff
            hours = remaining.seconds // 3600
            minutes = (remaining.seconds % 3600) // 60
            
            keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                get_text(user_id, 'farm_cooldown', hours=hours, minutes=minutes),
                reply_markup=reply_markup
            )
            return
    
    # Generate random star reward (0.1-3 stars)
    # Common: 0.1-2 stars (70% chance)
    # Rare: 2-3 stars (30% chance)
    if random.random() < 0.7:
        # Common drop
        stars_reward = round(random.uniform(0.1, 2.0), 1)
    else:
        # Rare drop
        stars_reward = round(random.uniform(2.0, 3.0), 1)
    
    # Set farm cooldown and store pending reward
    user_data['last_farm'] = datetime.now().isoformat()
    user_data['pending_farm_reward'] = {
        'stars': stars_reward,
        'views': 1,
        'task': random.choice(FARM_TASKS),
        'created_at': datetime.now().isoformat()
    }
    update_user_data(user_id, user_data)
    
    # Show task to complete
    keyboard = [
        [InlineKeyboardButton(get_text(user_id, 'task_done'), callback_data="farm_task_done")],
        [InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        get_text(user_id, 'farm_reward', stars=stars_reward) + f"\n\n📝 {user_data['pending_farm_reward']['task']}",
        reply_markup=reply_markup
    )

async def handle_tasks_callback(query, context: ContextTypes.DEFAULT_TYPE):
    user_id = query.from_user.id
    user_data = get_user_data(user_id)
    data = load_data()

    # Check if user has a current task
    if user_data.get('current_task'):
        if user_data['current_task'].startswith('admin_task_'):
            # Handle admin task
            task_id = user_data['current_task']
            admin_tasks = data.get('admin_tasks', [])
            task = next((t for t in admin_tasks if t['id'] == task_id), None)
            
            if task:
                keyboard = [
                    [InlineKeyboardButton(get_text(user_id, 'task_done'), callback_data=f"admin_task_done_{task_id}")],
                    [InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(
                    f"📝 {task['description']}\n⭐ Reward: {task['reward']} stars\n\n🔗 Link: {task['link']}\n\nComplete this task and press 'Done'",
                    reply_markup=reply_markup
                )
            else:
                user_data['current_task'] = None
                update_user_data(user_id, user_data)
                await handle_tasks_callback(query, context)
        else:
            # Handle channel subscription task
            channel = user_data['current_task']
            keyboard = [
                [InlineKeyboardButton(get_text(user_id, 'task_done'), callback_data=f"task_done_{channel}")],
                [InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                get_text(user_id, 'task_subscribe', channel=channel),
                reply_markup=reply_markup
            )
    else:
        # First check for available admin tasks
        admin_tasks = data.get('admin_tasks', [])
        completed_admin_tasks = user_data.get('completed_admin_tasks', [])
        available_admin_tasks = [t for t in admin_tasks if t['id'] not in completed_admin_tasks]
        
        if available_admin_tasks:
            # Assign first available admin task
            task = available_admin_tasks[0]
            user_data['current_task'] = task['id']
            update_user_data(user_id, user_data)
            
            keyboard = [
                [InlineKeyboardButton(get_text(user_id, 'task_done'), callback_data=f"admin_task_done_{task['id']}")],
                [InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"📝 {task['description']}\n⭐ Reward: {task['reward']} stars\n\n🔗 Link: {task['link']}\n\nComplete this task and press 'Done'",
                reply_markup=reply_markup
            )
        else:
            # Then check for channel subscription tasks
            channels = data.get('channels', CHANNELS)
            completed_channels = list(user_data.get('subscriptions', {}).keys())
            available_channels = [ch for ch in channels if ch not in completed_channels]

            if available_channels:
                channel = available_channels[0]
                user_data['current_task'] = channel
                update_user_data(user_id, user_data)

                keyboard = [
                    [InlineKeyboardButton(get_text(user_id, 'task_done'), callback_data=f"task_done_{channel}")],
                    [InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(
                    get_text(user_id, 'task_subscribe', channel=channel),
                    reply_markup=reply_markup
                )
            else:
                keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data="back_menu")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(
                    get_text(user_id, 'no_tasks'),
                    reply_markup=reply_markup
                )
async def check_subscriptions(context: ContextTypes.DEFAULT_TYPE):
    admin_id = 1443301925  # твой ID
    await context.bot.send_message(chat_id=admin_id, text="Проверка подписок прошла!")
def main():
    if not BOT_TOKEN:
        logger.error("ERROR: Please set BOT_TOKEN environment variable in Secrets")
        print("ERROR: Please set BOT_TOKEN environment variable in Secrets")
        return
    
    try:
        # Загружаем данные (твоя функция load_data должна быть в коде)
        data = load_data()
        data['channels'] = CHANNELS  # CHANNELS — у тебя должен быть этот список или словарь с каналами
        if 'banned_users' not in data:
            data['banned_users'] = []
        save_data(data)  # Твоя функция сохранения данных

        # Создаем приложение бота с токеном
        application = Application.builder().token(BOT_TOKEN).build()

        # Добавляем обработчики команд и сообщений
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("menu", menu_command))
        application.add_handler(CommandHandler("admin", admin_command))
        application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)^(menu|☰ menu|☰ меню|☰ меню|☰ menü)$'), menu_command))
        application.add_handler(CallbackQueryHandler(handle_callback))
        application.add_handler(PreCheckoutQueryHandler(precheckout_callback))
        application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))

        # Запускаем периодическую проверку подписок (если есть функция check_subscriptions)
        application.job_queue.run_repeating(check_subscriptions, interval=3600, first=60)

        logger.info("Bot started and listening for messages...")
        print("Bot started and listening for messages...")

        # Запускаем поллинг бота
        application.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        print(f"Error starting bot: {e}")
        raise

if __name__ == '__main__':
    main()
