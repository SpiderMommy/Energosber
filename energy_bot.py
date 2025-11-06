import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен бота
TOKEN = "7833930614:AAET_Lq5B4itg-1Dwzi2Ne3g-UylYK9jUQE"

# Советы по энергосбережению
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

# Факты об энергосбережении
FACTS = [
    "💡 Знаешь ли ты? Энергосберегающая лампа служит в 8 раз дольше обычной!",
    "💧 Выключая воду при чистке зубов, ты экономишь до 10 литров воды!",
    "🌍 Экономя энергию, ты помогаешь сохранить природу Беларуси!",
    "💰 Семья из 3 человек может сэкономить до 50% на коммунальных услугах!",
    "🔋 Батарейки, выброшенные в природу, загрязняют 20 м² земли!",
    "📊 Беларусь экономит энергию, как 2 атомные электростанции в год!",
    "🚲 1 сэкономленный кВт·ч = 10 км на велосипеде без вреда для природы!"
]

# Команда /start
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

    # Создаем клавиатуру
    keyboard = [
        [KeyboardButton("💡 Советы по экономии"), KeyboardButton("🌍 Интересные факты")],
        [KeyboardButton("🎮 Игра-викторина"), KeyboardButton("🏆 Эко-челлендж")],
        [KeyboardButton("📚 Полезные ссылки"), KeyboardButton("ℹ️ О проекте")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📖 Доступные команды:

💡 Советы по экономии - практические советы
🌍 Интересные факты - удивительные факты об энергии
🎮 Игра-викторина - проверь свои знания
🏆 Эко-челлендж - задания на каждый день
📚 Полезные ссылки - ресурсы для учебы
ℹ️ О проекте - информация о боте

Или просто напиши мне вопрос!
    """
    await update.message.reply_text(help_text)

# Обработчик кнопки "Советы по экономии"
async def show_tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tips_keyboard = [
        [KeyboardButton("⚡ Электричество"), KeyboardButton("💧 Вода")],
        [KeyboardButton("🔥 Отопление"), KeyboardButton("📺 Приборы")],
        [KeyboardButton("🔙 Назад")]
    ]
    reply_markup = ReplyKeyboardMarkup(tips_keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Выбери категорию советов:",
        reply_markup=reply_markup
    )

# Показ конкретных советов
async def show_category_tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = update.message.text.lower()

    if category in ["⚡ электричество", "электричество"]:
        tips = ENERGY_TIPS["электричество"]
        category_name = "⚡ Электричество"
    elif category in ["💧 вода", "вода"]:
        tips = ENERGY_TIPS["вода"]
        category_name = "💧 Вода"
    elif category in ["🔥 отопление", "отопление"]:
        tips = ENERGY_TIPS["отопление"]
        category_name = "🔥 Отопление"
    elif category in ["📺 приборы", "приборы"]:
        tips = ENERGY_TIPS["приборы"]
        category_name = "📺 Приборы"
    else:
        return

    tips_text = f"{category_name} - полезные советы:\n\n" + "\n".join([f"• {tip}" for tip in tips])
    await update.message.reply_text(tips_text)

# Обработчик кнопки "Интересные факты"
async def show_facts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import random
    fact = random.choice(FACTS)
    await update.message.reply_text(fact)

# Обработчик кнопки "Игра-викторина"
async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quiz_questions = [
        {
            "question": "Что экономит больше энергии?",
            "options": ["Энергосберегающая лампа", "Обычная лампа", "Свеча"],
            "answer": 0
        },
        {
            "question": "Как правильно проветривать комнату?",
            "options": ["Открыть окно на 2 часа", "Открыть на 5-10 минут полностью", "Не проветривать вообще"],
            "answer": 1
        },
        {
            "question": "Что нужно делать с зарядным устройством?",
            "options": ["Оставлять в розетке всегда", "Вынимать после зарядки", "Ничего не делать"],
            "answer": 1
        }
    ]

    # Сохраняем вопросы в контекст
    context.user_data['quiz'] = quiz_questions
    context.user_data['current_question'] = 0
    context.user_data['score'] = 0

    await ask_question(update, context)

async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quiz = context.user_data['quiz']
    current = context.user_data['current_question']

    if current >= len(quiz):
        # Конец викторины
        score = context.user_data['score']
        total = len(quiz)
        await update.message.reply_text(
            f"🎉 Викторина завершена!\n"
            f"Твой результат: {score}/{total}\n"
            f"{'Отлично! Ты настоящий энергосберегатель! 🌟' if score == total else 'Хорошо, но есть куда расти! 📚'}"
        )
        await start(update, context)
        return

    question_data = quiz[current]
    options = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(question_data['options'])])

    quiz_text = f"❓ Вопрос {current + 1}:\n{question_data['question']}\n\n{options}"

    # Клавиатура для ответов
    keyboard = [[KeyboardButton(str(i+1)) for i in range(len(question_data['options']))]]
    keyboard.append([KeyboardButton("🔙 Отмена")])
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(quiz_text, reply_markup=reply_markup)

async def handle_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.message.text

    if answer == "🔙 Отмена":
        await start(update, context)
        return

    if not answer.isdigit():
        await update.message.reply_text("Пожалуйста, выбери номер ответа!")
        return

    user_answer = int(answer) - 1
    current = context.user_data['current_question']
    quiz = context.user_data['quiz']

    if user_answer == quiz[current]['answer']:
        context.user_data['score'] += 1
        await update.message.reply_text("✅ Правильно! Молодец!")
    else:
        correct_answer = quiz[current]['options'][quiz[current]['answer']]
        await update.message.reply_text(f"❌ Неправильно. Правильный ответ: {correct_answer}")

    context.user_data['current_question'] += 1
    await ask_question(update, context)

# Обработчик кнопки "Эко-челлендж"
async def start_challenge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    challenges = [
        "🎯 Задание на сегодня: выключать свет, выходя из комнаты",
        "🎯 Задание: принимать душ не более 5 минут",
        "🎯 Задание: вынуть все неиспользуемые зарядки из розеток",
        "🎯 Задание: рассказать другу о одном способе экономии энергии",
        "🎯 Задание: проверить, нет ли протекающих кранов"
    ]

    import random
    challenge = random.choice(challenges)

    await update.message.reply_text(
        f"🏆 Эко-челлендж!\n\n{challenge}\n\n"
        "Выполни задание и возвращайся за новым! 🌟"
    )

# Обработчик кнопки "Полезные ссылки"
async def show_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    links_text = """
📚 Полезные ресурсы об энергосбережении:

• energo.gov.by - Министерство энергетики Беларуси
• energosbereg.by - Республиканский центр энергосбережения
• un.org/sustainabledevelopment - Цели устойчивого развития ООН
• greenbelarus.info - Экологические инициативы в Беларуси

📱 Для учебы:
• energykids.eu - Игры и задания для детей
• ecoby.org - Экологическое образование
    """
    await update.message.reply_text(links_text)

# Обработчик кнопки "О проекте"
async def about_project(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = """
ℹ️ О проекте «Энергосберегайка»

Этот бот создан для школьников Беларуси, чтобы:
• Научить экономить энергию и ресурсы
• Показать важность энергосбережения
• Сделать обучение интересным и интерактивным

💚 Сохраним энергию для будущего Беларуси вместе!
    """
    await update.message.reply_text(about_text)

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if text in ["💡 советы по экономии", "советы"]:
        await show_tips(update, context)
    elif text in ["🌍 интересные факты", "факты"]:
        await show_facts(update, context)
    elif text in ["🎮 игра-викторина", "викторина", "игра"]:
        await start_quiz(update, context)
    elif text in ["🏆 эко-челлендж", "челлендж"]:
        await start_challenge(update, context)
    elif text in ["📚 полезные ссылки", "ссылки"]:
        await show_links(update, context)
    elif text in ["ℹ️ о проекте", "о боте"]:
        await about_project(update, context)
    elif text in ["🔙 назад", "назад", "🔙"]:
        await start(update, context)
    elif text in ENERGY_TIPS or text in ["⚡ электричество", "💧 вода", "🔥 отопление", "📺 приборы"]:
        await show_category_tips(update, context)
    elif text.isdigit() and 'quiz' in context.user_data:
        await handle_quiz_answer(update, context)
    else:
        await update.message.reply_text(
            "Я пока не понимаю эту команду. Используй кнопки меню или напиши /help для помощи!"
        )

# Основная функция
def main():
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    print("Бот 'Энергосберегайка' запущен!")
    application.run_polling()

if __name__ == '__main__':
    main()
