import os
import logging
import random
import threading
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Создаем Flask приложение для здоровья сервиса
app = Flask(__name__)

@app.route('/')
def health_check():
    return "🤖 Бот Энергосберегайка работает! Status: OK"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
# Токен бота
BOT_TOKEN = "7833930614:AAET_Lq5B4itg-1Dwzi2Ne3g-UylYK9jUQE"

# Данные бота
ENERGY_TIPS = {
    "электричество": [
        "🔌 Выключай свет, когда выходишь из комнаты",
        "💡 Используй энергосберегающие лампы - они экономят до 80% энергии",
        "📱 Отключай зарядные устройства из розетки после использования",
        "🖥️ Настраивай режим энергосбережения на компьютере и телефоне",
        "❄️ Холодильник ставь подальше от батарей и плиты"
    ],
    "вода": [
        "🚿 Принимай душ вместо ванны - экономия до 100 литров воды!",
        "🚰 Закрывай кран, когда чистишь зубы",
        "💧 Используй посудомоечную машину только при полной загрузке",
        "🔧 Проверяй, нет ли протечек в кранах",
        "🌧️ Собирай дождевую воду для полива растений"
    ],
    "отопление": [
        "🏠 Утепли окна и двери - это сохранит тепло",
        "🌡️ Оптимальная температура в комнате - 20-22°C",
        "🔆 Не закрывай батареи мебелью или шторами",
        "🪟 Проветривай комнату интенсивно, но недолго (5-10 минут)",
        "🧹 Регулярно чисти батареи от пыли"
    ],
    "приборы": [
        "📺 Выключай телевизор и компьютер полностью, а не в режиме standby",
        "🍳 Готовь с закрытой крышкой - это экономит энергию",
        "🔥 Используй посуду с плоским дном на электроплитах",
        "🧊 Размораживай холодильник регулярно",
        "🌬️ Чисти фильтры кондиционера и пылесоса"
    ]
}

FACTS = [
    "💡 Энергосберегающая лампа служит в 8 раз дольше обычной!",
    "💧 Выключая воду при чистке зубов, ты экономишь до 10 литров воды!",
    "🌍 Экономя энергию, ты помогаешь сохранить природу Беларуси!",
    "💰 Семья из 3 человек может сэкономить до 50% на коммунальных услугах!",
    "🔋 Батарейки, выброшенные в природу, загрязняют 20 м² земли!"
]

# Команды бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = f"""
🤖 Привет, {user.first_name}! Я бот «Энергосберегайка»!

Я помогу тебе узнать:
• Как экономить энергию дома и в школе
• Интересные факты об энергосбережении  
• Почему это важно для Беларуси

Выбери, что тебя интересует! 🌟
    """
    
    keyboard = [
        [KeyboardButton("💡 Советы"), KeyboardButton("🌍 Факты")],
        [KeyboardButton("🎮 Викторина"), KeyboardButton("🏆 Челлендж")],
        [KeyboardButton("📚 Ссылки"), KeyboardButton("ℹ️ О проекте")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📖 Доступные команды:

/start - Запустить бота
/help - Помощь

Или используй кнопки меню!
    """
    await update.message.reply_text(help_text)

async def show_tips_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tips_keyboard = [
        [KeyboardButton("⚡ Электричество"), KeyboardButton("💧 Вода")],
        [KeyboardButton("🔥 Отопление"), KeyboardButton("📺 Приборы")],
        [KeyboardButton("🔙 Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(tips_keyboard, resize_keyboard=True)
    await update.message.reply_text("Выбери категорию советов:", reply_markup=reply_markup)

async def show_tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    category_map = {
        "⚡ Электричество": "электричество",
        "💧 Вода": "вода", 
        "🔥 Отопление": "отопление",
        "📺 Приборы": "приборы"
    }
    
    if text in category_map:
        category = category_map[text]
        tips = ENERGY_TIPS[category]
        tips_text = f"{text} - полезные советы:\n\n" + "\n".join([f"• {tip}" for tip in tips])
        await update.message.reply_text(tips_text)
    else:
        await update.message.reply_text("Пожалуйста, выбери категорию из меню")

async def show_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fact = random.choice(FACTS)
    await update.message.reply_text(fact)

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    questions = [
        {
            "question": "Что экономит больше энергии?",
            "options": ["Энергосберегающая лампа", "Обычная лампа", "Свеча"],
            "answer": 0
        },
        {
            "question": "Как правильно проветривать комнату?",
            "options": ["Открыть окно на 2 часа", "Открыть на 5-10 минут полностью", "Не проветривать"],
            "answer": 1
        },
        {
            "question": "Что нужно делать с зарядным устройством?",
            "options": ["Оставлять в розетке всегда", "Вынимать после зарядки", "Ничего не делать"],
            "answer": 1
        }
    ]
    
    context.user_data['quiz_questions'] = questions
    context.user_data['quiz_index'] = 0
    context.user_data['quiz_score'] = 0
    
    await ask_quiz_question(update, context)

async def ask_quiz_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    questions = context.user_data.get('quiz_questions', [])
    index = context.user_data.get('quiz_index', 0)
    
    if index >= len(questions):
        score = context.user_data.get('quiz_score', 0)
        total = len(questions)
        result_text = f"🎉 Викторина завершена!\nТвой результат: {score}/{total}\n"
        
        if score == total:
            result_text += "Отлично! Ты настоящий энергосберегатель! 🌟"
        else:
            result_text += "Хорошо, но есть куда расти! 📚"
            
        await update.message.reply_text(result_text)
        await start(update, context)
        return
    
    question = questions[index]
    options_text = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(question['options'])])
    quiz_text = f"❓ Вопрос {index + 1}:\n{question['question']}\n\n{options_text}"
    
    keyboard = [[KeyboardButton(str(i+1)) for i in range(len(question['options']))]]
    keyboard.append([KeyboardButton("🔙 Отмена")])
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(quiz_text, reply_markup=reply_markup)

async def handle_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.message.text
    
    if answer == "🔙 Отмена":
        await start(update, context)
        return
    
    if not answer.isdigit():
        await update.message.reply_text("Пожалуйста, выбери номер ответа (1, 2, 3)")
        return
    
    questions = context.user_data.get('quiz_questions', [])
    index = context.user_data.get('quiz_index', 0)
    
    if index < len(questions):
        user_answer = int(answer) - 1
        correct_answer = questions[index]['answer']
        
        if user_answer == correct_answer:
            context.user_data['quiz_score'] = context.user_data.get('quiz_score', 0) + 1
            await update.message.reply_text("✅ Правильно! Молодец!")
        else:
            correct_text = questions[index]['options'][correct_answer]
            await update.message.reply_text(f"❌ Неправильно. Правильный ответ: {correct_text}")
        
        context.user_data['quiz_index'] = index + 1
        await ask_quiz_question(update, context)

async def start_challenge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    challenges = [
        "🎯 Задание: выключать свет, выходя из комнаты",
        "🎯 Задание: принимать душ не более 5 минут", 
        "🎯 Задание: вынуть неиспользуемые зарядки из розеток",
        "🎯 Задание: рассказать другу о способе экономии энергии",
        "🎯 Задание: проверить, нет ли протекающих кранов"
    ]
    
    challenge = random.choice(challenges)
    await update.message.reply_text(f"🏆 Эко-челлендж!\n\n{challenge}\n\nВыполни и возвращайся за новым! 🌟")

async def show_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    links_text = """
📚 Полезные ресурсы:

• minenergo.gov.by - Министерство энергетики Беларуси
• energoeffect.gov.by - Департамент по энергосбережению
• @energoeffectgovby - telegram-канал Департамента по энергосбережению

💚 Сохраним энергию для будущего Беларуси!
    """
    await update.message.reply_text(links_text)

async def about_project(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = """
ℹ️ О проекте «Энергосберегайка»

Бот для школьников Беларуси:
• Учим экономить энергию
• Показываем важность энергосбережения  
• Делаем обучение интересным
    """
    await update.message.reply_text(about_text)

# Главный обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "💡 Советы":
        await show_tips_menu(update, context)
    elif text == "🌍 Факты":
        await show_fact(update, context)
    elif text == "🎮 Викторина":
        await start_quiz(update, context)
    elif text == "🏆 Челлендж":
        await start_challenge(update, context)
    elif text == "📚 Ссылки":
        await show_links(update, context)
    elif text == "ℹ️ О проекте":
        await about_project(update, context)
    elif text in ["⚡ Электричество", "💧 Вода", "🔥 Отопление", "📺 Приборы"]:
        await show_tips(update, context)
    elif text == "🔙 Назад":
        await start(update, context)
    elif text.isdigit() and 'quiz_questions' in context.user_data:
        await handle_quiz_answer(update, context)
    else:
        await update.message.reply_text("Используй кнопки меню или /help для помощи!")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Ошибка: {context.error}")

def main():
    print("🚀 Запуск бота Энергосберегайка...")
    
    try:
        # Создаем приложение
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Добавляем обработчики
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_error_handler(error_handler)
        
        # Запускаем бота
        print("=" * 50)
        print("🤖 Бот 'Энергосберегайка' успешно запущен!")
        print("📍 Работает на Render.com")
        print("⚡ Готов к приему сообщений")
        print("=" * 50)
        
        application.run_polling()
        
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")

def main():
    """Основная функция - запускает и бота, и HTTP-сервер"""
    # Запускаем Flask в отдельном потоке
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("🌐 HTTP-сервер запущен для проверки здоровья")
    
    # Запускаем бота в основном потоке
    run_bot()

if __name__ == '__main__':
    main()
