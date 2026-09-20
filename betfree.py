import telebot
from telebot import types
from datetime import datetime
import random

TOKEN = "8733342946:AAFGsFp5D5eiDlWDQeGULssA8obYTgq7wbY"

bot = telebot.TeleBot(TOKEN)

users = {}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {
            "days_clean": 0,
            "total_spent": 0,
            "last_checkin": None,
        }
    return users[user_id]

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    get_user(user_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("✅ Сьогодні без гри", "❌ Був зрив")
    markup.add("📊 Моя статистика", "💰 Додати витрати")
    markup.add("💪 Мотивація", "📞 Допомога")
    bot.send_message(message.chat.id,
        "👋 Привіт! Я BetFree — помічник у боротьбі з ігровою залежністю.\n\n"
        "Тут можна:\n"
        "✅ Відстежувати дні без гри\n"
        "💰 Бачити скільки вдалося зекономити\n"
        "💪 Отримувати підтримку\n\n"
        "Ти не одна/один у цьому. Починаємо разом 🤝",
        reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "✅ Сьогодні без гри")
def checkin_success(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    today = datetime.now().strftime("%Y-%m-%d")
    if user["last_checkin"] != today:
        user["days_clean"] += 1
        user["last_checkin"] = today
    days = user["days_clean"]
    bot.send_message(message.chat.id,
        f"🎉 Відмінно! Вже {days} {'день' if days == 1 else 'дні' if days < 5 else 'днів'} без гри!\n\n"
        f"Кожен день — це перемога 💪\n"
        f"Так тримати!")

@bot.message_handler(func=lambda m: m.text == "❌ Був зрив")
def checkin_fail(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    user["days_clean"] = 0
    bot.send_message(message.chat.id,
        "😔 Нічого страшного. Це частина шляху.\n\n"
        "Найважливіше — що є бажання змінитись.\n"
        "Завтра — новий день і новий шанс 🌅\n\n"
        "Головне — не зупинятись.")

@bot.message_handler(func=lambda m: m.text == "📊 Моя статистика")
def stats(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    days = user["days_clean"]
    spent = user["total_spent"]
    bot.send_message(message.chat.id,
        f"📊 Статистика:\n\n"
        f"🗓 Днів без гри: {days}\n"
        f"💰 Витрачено на гру: {spent} грн\n"
        f"💚 Орієнтовна економія за {days} днів: {days * 200} грн\n\n"
        f"Кожен день без гри — це гроші, які залишаються з тобою!")

@bot.message_handler(func=lambda m: m.text == "💰 Додати витрати")
def add_expense(message):
    bot.send_message(message.chat.id,
        "Введи суму яку було витрачено на гру (тільки цифри):")
    bot.register_next_step_handler(message, save_expense)

def save_expense(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    try:
        amount = float(message.text)
        user["total_spent"] += amount
        bot.send_message(message.chat.id,
            f"💰 Записано: {amount} грн\n"
            f"Загалом витрачено: {user['total_spent']} грн\n\n"
            f"Ці гроші могли піти на щось важливе.")
    except:
        bot.send_message(message.chat.id,
            "Введи будь ласка тільки число, наприклад: 500")

@bot.message_handler(func=lambda m: m.text == "💪 Мотивація")
def motivation(message):
    quotes = [
        "Кожен день без гри — це день, коли є контроль над своїм життям 💪",
        "Сила — це не відсутність спокус, а вміння їм протистояти 🔥",
        "Свобода починається з одного рішення. Це рішення вже прийнято 🌟",
        "Гроші, які не програні — це гроші, що працюють на тебе 💰",
        "Найкраща ставка — це ставка на власне майбутнє ✨",
        "Маленькі кроки щодня — великі зміни з часом 🚀"
    ]
    bot.send_message(message.chat.id, random.choice(quotes))

@bot.message_handler(func=lambda m: m.text == "📞 Допомога")
def help_info(message):
    bot.send_message(message.chat.id,
        "📞 Якщо потрібна допомога:\n\n"
        "🇺🇦 Гаряча лінія з психічного здоров'я:\n"
	"0-800-505-679 (безкоштовно)\n\n"
        "💬 Також можна написати сюди — BetFree завжди поруч.")

print("BetFree бот запущено!")
bot.infinity_polling()