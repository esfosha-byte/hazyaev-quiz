import os
import random

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes


# =========================
# НАСТРОЙКИ
# =========================

CHANNEL_USERNAME = "@tgxaxyeva"
CHANNEL_URL = "https://t.me/tgxaxyeva"


# =========================
# ПЕРСОНАЖИ
# =========================

RESULTS = {
    "Кореш": {
        "emoji": "🔥",
        "description": "Ты живёшь эмоциями, любишь движ и умеешь превращать обычную ситуацию в историю."
    },
    "Парадеевич": {
        "emoji": "👑",
        "description": "Ты человек-движ. Любишь собирать людей вокруг себя и превращать идеи в реальные события."
    },
    "Куертов": {
        "emoji": "💰",
        "description": "Ты замечаешь возможности там, где другие их не видят. Выгода, результат и движение вперёд — твоё."
    },
    "Плохой Парень": {
        "emoji": "😈",
        "description": "У тебя свой характер и свои правила. Ты не особо любишь подстраиваться под окружающих."
    },
    "Exile": {
        "emoji": "🧠",
        "description": "Ты наблюдатель и стратег. Сначала разбираешься в ситуации, а потом действуешь."
    },
    "Frame Tamer": {
        "emoji": "🤡",
        "description": "Ты способен превратить практически любую ситуацию в контент. Абсурд и неожиданные повороты — твоя стихия."
    },
    "Данила Горилла": {
        "emoji": "🦍",
        "description": "Ты человек действия. Меньше разговоров — больше движухи и приключений."
    }
}


# =========================
# ВОПРОСЫ
# =========================

QUESTIONS = [
    {
        "text": "🏠 Вы приехали с Хазяевами в новый город. Что делаешь первым?",
        "answers": [
            ("🔥 Иду искать приключения", {"Кореш": 3, "Данила Горилла": 2}),
            ("💰 Смотрю, где можно что-нибудь замутить", {"Куертов": 3}),
            ("👑 Собираю всех и решаю, чем занимаемся", {"Парадеевич": 3}),
            ("🍻 Ищу место для максимального угара", {"Плохой Парень": 3}),
            ("🧠 Сначала осматриваюсь", {"Exile": 3}),
            ("🤡 Ищу повод для контента", {"Frame Tamer": 3})
        ]
    },
    {
        "text": "🎥 Тебе предлагают сняться в безумном челлендже. Что делаешь?",
        "answers": [
            ("«А когда начинаем?»", {"Кореш": 3}),
            ("«А сколько платят?»", {"Куертов": 3}),
            ("«Давайте сделаем ещё безумнее»", {"Frame Tamer": 3}),
            ("«Если все идут — я тоже»", {"Данила Горилла": 3}),
            ("«Сначала объясните правила»", {"Exile": 3}),
            ("«Погнали, будет движ»", {"Парадеевич": 3})
        ]
    },
    {
        "text": "😂 Друг попал в максимально тупую ситуацию. Твоя реакция?",
        "answers": [
            ("Сначала смеюсь, потом помогаю", {"Кореш": 3}),
            ("Снимаю происходящее", {"Frame Tamer": 3}),
            ("Пытаюсь быстро решить проблему", {"Парадеевич": 3}),
            ("Добавляю ещё немного хаоса", {"Плохой Парень": 3}),
            ("Анализирую, как мы вообще сюда попали", {"Exile": 3}),
            ("«Ну всё, приключение началось»", {"Данила Горилла": 3})
        ]
    },
    {
        "text": "💸 У тебя неожиданно появляется 1 000 000 ₽. Что делаешь?",
        "answers": [
            ("Потрачу на мечту", {"Кореш": 3}),
            ("Вложу и попробую сделать ещё больше", {"Куертов": 3}),
            ("Запущу какой-нибудь проект", {"Парадеевич": 3}),
            ("Устрою легендарный отдых", {"Данила Горилла": 3}),
            ("Буду думать, как увеличить сумму", {"Exile": 3}),
            ("Сделаю из этого контент", {"Frame Tamer": 3})
        ]
    },
    {
        "text": "😈 Тебя публично провоцируют. Твоя реакция?",
        "answers": [
            ("Отшучусь", {"Кореш": 3}),
            ("Спокойно объясню позицию", {"Exile": 3}),
            ("Отвечу жёстко", {"Плохой Парень": 3}),
            ("Превращу конфликт в контент", {"Frame Tamer": 3}),
            ("Использую ситуацию себе на пользу", {"Куертов": 3}),
            ("Соберу всех и разрулю", {"Парадеевич": 3})
        ]
    },
    {
        "text": "🍻 Какой отдых тебе ближе?",
        "answers": [
            ("Большая компания и максимальный угар", {"Плохой Парень": 3}),
            ("Путешествие и новые впечатления", {"Данила Горилла": 3}),
            ("Тусовка, где я задаю темп", {"Парадеевич": 3}),
            ("Дома со своими людьми", {"Exile": 3}),
            ("Что-нибудь максимально спонтанное", {"Frame Tamer": 3}),
            ("Главное — чтобы было весело", {"Кореш": 3})
        ]
    },
    {
        "text": "🤝 Что для тебя самое важное в компании друзей?",
        "answers": [
            ("Чтобы всегда было весело", {"Кореш": 3}),
            ("Чтобы люди были настоящими", {"Exile": 3}),
            ("Чтобы вместе делать большие вещи", {"Парадеевич": 3}),
            ("Чтобы никто не боялся быть собой", {"Плохой Парень": 3}),
            ("Чтобы каждый был готов к безумию", {"Frame Tamer": 3}),
            ("Чтобы всегда был движ", {"Данила Горилла": 3})
        ]
    },
    {
        "text": "🚗 Машина сломалась посреди дороги. Что делаешь?",
        "answers": [
            ("«Ну всё, приключение началось»", {"Кореш": 3}),
            ("Ищу человека, который быстро решит проблему", {"Парадеевич": 3}),
            ("Пытаюсь разобраться сам", {"Данила Горилла": 3}),
            ("Снимаю происходящее", {"Frame Tamer": 3}),
            ("Спокойно ищу оптимальное решение", {"Exile": 3}),
            ("Думаю, как извлечь из ситуации пользу", {"Куертов": 3})
        ]
    },
    {
        "text": "💡 Что тебе ближе?",
        "answers": [
            ("Жить эмоциями", {"Кореш": 3}),
            ("Всегда искать возможность", {"Куертов": 3}),
            ("Создавать движ вокруг себя", {"Парадеевич": 3}),
            ("Делать всё по-своему", {"Плохой Парень": 3}),
            ("Постоянно искать новые приколы", {"Frame Tamer": 3}),
            ("Всегда быть готовым к приключениям", {"Данила Горилла": 3})
        ]
    },
    {
        "text": "🏆 Какой фразой друзья описали бы тебя?",
        "answers": [
            ("«С ним никогда не бывает скучно»", {"Кореш": 3}),
            ("«Он всегда что-то мутит»", {"Парадеевич": 3}),
            ("«Он умеет находить выгоду»", {"Куертов": 3}),
            ("«Ему вообще похуй»", {"Плохой Парень": 3}),
            ("«Он может превратить всё в прикол»", {"Frame Tamer": 3}),
            ("«Он всегда готов к движу»", {"Данила Горилла": 3})
        ]
    }
]


# =========================
# ПРОВЕРКА ПОДПИСКИ
# =========================

async def is_subscribed(user_id, context):
    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )

        return member.status in ["creator", "administrator", "member"]

    except Exception as error:
        print("Ошибка проверки подписки:", error)
        return False


def subscription_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📢 ПОДПИСАТЬСЯ НА КАНАЛ",
                url=CHANNEL_URL
            )
        ],
        [
            InlineKeyboardButton(
                "✅ Я ПОДПИСАЛСЯ",
                callback_data="check_subscription"
            )
        ]
    ])


async def show_subscription(update):
    text = (
        "🏠 <b>КТО ТЫ ИЗ ХАЗЯЕВ?</b>\n\n"
        "Чтобы пройти тест, сначала подпишись на канал 👇\n\n"
        "После подписки нажми "
        "«✅ Я ПОДПИСАЛСЯ»."
    )

    if update.message:
        await update.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=subscription_keyboard()
        )
    else:
        await update.callback_query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=subscription_keyboard()
        )


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if not await is_subscribed(user_id, context):
        await show_subscription(update)
        return

    context.user_data.clear()
    context.user_data["question"] = 0
    context.user_data["scores"] = {
        character: 0 for character in RESULTS
    }

    await send_question(update, context)


# =========================
# ВОПРОСЫ
# =========================

def question_keyboard(number):

    buttons = []

    for index, (answer, _) in enumerate(
        QUESTIONS[number]["answers"]
    ):
        buttons.append([
            InlineKeyboardButton(
                answer,
                callback_data=f"answer:{number}:{index}"
            )
        ])

    return InlineKeyboardMarkup(buttons)


async def send_question(update, context):

    number = context.user_data["question"]
    question = QUESTIONS[number]

    text = (
        f"❓ <b>Вопрос {number + 1}/{len(QUESTIONS)}</b>\n\n"
        f"{question['text']}"
    )

    keyboard = question_keyboard(number)

    if update.message:
        await update.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=keyboard
        )
    else:
        await update.callback_query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=keyboard
        )


# =========================
# КНОПКИ
# =========================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # Проверка подписки
    if query.data == "check_subscription":

        if not await is_subscribed(user_id, context):

            await query.answer(
                "❌ Подписка не найдена. Подпишись на канал и попробуй ещё раз.",
                show_alert=True
            )

            return

        context.user_data.clear()
        context.user_data["question"] = 0
        context.user_data["scores"] = {
            character: 0 for character in RESULTS
        }

        await query.edit_message_text(
            "🔥 <b>Подписка подтверждена!</b>\n\n"
            "Погнали узнавать, кто ты из Хазяев 😈",
            parse_mode="HTML"
        )

        await send_question(update, context)

        return

    # Повторное прохождение
    if query.data == "restart":

        if not await is_subscribed(user_id, context):
            await show_subscription(update)
            return

        context.user_data.clear()
        context.user_data["question"] = 0
        context.user_data["scores"] = {
            character: 0 for character in RESULTS
        }

        await send_question(update, context)

        return

    # Ответ на вопрос
    if query.data.startswith("answer:"):

        if not await is_subscribed(user_id, context):
            await show_subscription(update)
            return

        _, question_number, answer_number = query.data.split(":")

        question_number = int(question_number)
        answer_number = int(answer_number)

        answer_scores = QUESTIONS[question_number]["answers"][
            answer_number
        ][1]

        for character, points in answer_scores.items():
            context.user_data["scores"][character] += points

        next_question = question_number + 1
        context.user_data["question"] = next_question

        if next_question >= len(QUESTIONS):
            await show_result(query, context)
        else:
            await send_question(update, context)


# =========================
# РЕЗУЛЬТАТ
# =========================

async def show_result(query, context):

    scores = context.user_data["scores"]

    max_score = max(scores.values())

    winners = [
        character
        for character, score in scores.items()
        if score == max_score
    ]

    winner = random.choice(winners)
    result = RESULTS[winner]

    text = (
        f"{result['emoji']} <b>ТЫ — {winner.upper()}!</b>\n\n"
        f"{result['description']}\n\n"
        "🔥 <b>Тест завершён!</b>"
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔄 ПРОЙТИ ЕЩЁ РАЗ",
                callback_data="restart"
            )
        ],
        [
            InlineKeyboardButton(
                "📢 ХАЗЯЕВА STREAM",
                url=CHANNEL_URL
            )
        ]
    ])

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=keyboard
    )


# =========================
# ЗАПУСК
# =========================

def main():

    token = os.environ.get("BOT_TOKEN")

    if not token:
        raise RuntimeError("BOT_TOKEN не найден")

    application = (
        Application.builder()
        .token(token)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    print("Бот запущен!")

    application.run_polling()


if __name__ == "__main__":
    main()
