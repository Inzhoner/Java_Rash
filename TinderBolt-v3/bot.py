from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    CommandHandler,
)

from gpt import *  # type: ignore
from util import *  # type: ignore

TOKEN = "7549253403:AAHuUvEdbWpsOkSqi4a-v9nZZgSK1cyJhS0"


#  + тут будемо писати наш код :)
async def start(update, context):
    msg = load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, msg)
    await show_main_menu(
        update,
        context,
        {
            "start": "Головне меню",
            "profile": "Генерація Tinder-профіля \uD83D\uDD0E",
            "opener": "Повідомлення для знайомства \uD83D\uDCD7",
            "message": "Переписка від вашого імені \uD83D\uDCE8",
            "date": "Спілкування з зірками \uD83D\uDD25",
            "gpt": "Задати питання ChatGPT \uD83D\uDDE0",
        },
    )


# =функція gpt - обробник на команду gpt
async def gpt(update, context):
    dialog.mode = "gpt"
    await send_photo(update, context, "gpt")
    msg = load_message("gpt")
    await send_text(update, context, msg)


# =функція обробник команд date (буде переводити режим листування в режим date)
async def date(update, context):
    dialog.mode = "date"
    msg = load_message("date")
    await send_photo(update, context, "date")
    await send_text_buttons(
        update,
        context,
        msg,
        {
            "date_grande": "Аріана Гранде",
            "date_robbie": "Марго Роббі",
            "date_zendaya": "Зендея",
            "date_gosling": "Райан Гослінг",
            "date_hardy": "Том Харді",
        },
    )


# =функція оброблення натискання по кнопках date (запускає переписку з нашою зіркою)
async def date_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()  # повідомлення що ми натискали на кнопку
    await send_photo(update, context, query)
    await send_text(
        update,
        context,
        "Гарний вибір. Ваша задача запросити дівчину бо хлопця на побачення за 5 повідомлень",
    )
    prompt = load_prompt(query)
    chatgpt.set_prompt(prompt)


#  =функція для date діалогу
async def date_dialog(update, context):
    text = update.message.text
    my_message = await send_text(update, context, "Набираю повідомлення:")
    answer = await chatgpt.add_message(text)
    await my_message.edit_text(answer)


# =функція оброблення /message
async def message(update, context):
    dialog.mode = "message"
    msg = load_message("message")
    await send_photo(update, context, "message")
    await send_text_buttons(
        update,
        context,
        msg,
        {
            "message_next": "Написати повідомлення",
            "message_date": "Запросити на побачення",
        },
    )
    dialog.list.clear()


# =додавання усіх наших повідомлень в наш список []
async def message_dialog(update, context):
    text = update.message.text
    dialog.list.append(text)


# =обробник для натискання на кнопки "Написати повідомлення" та "Запросити на побачення"
async def message_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    prompt = load_prompt(query)
    user_chat_history = "\n\n".join(dialog.list)

    my_message = await send_text(update, context, "Думаю над варіантами відповідей...")
    answer = await chatgpt.send_question(prompt, user_chat_history)
    await my_message.edit_text(answer)


# =функція оброблення повідомлення до чату gpt
async def gpt_dialog(update, context):
    text = update.message.text
    promt = load_prompt("gpt")
    answer = await chatgpt.send_question(promt, text)
    await send_text(update, context, answer)


# =функція hello - відповідає на введення будь-якого тексту у боті
async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    elif dialog.mode == "date":
        await date_dialog(update, context)
    elif dialog.mode == "message":
        await message_dialog(update, context)


# !
#  region important - поки що прибираємо функцію  buttons_handler
# async def buttons_handler(update, context):
#     query = update.callback_query.data
#     if query == 'start':
#         await send_text(update, context, 'Started!')
#     elif query == 'stop':
#         await send_text(update, context, 'Stopped!')
#  endregion


dialog = Dialog()  # type: ignore
dialog.mode = None  # type: ignore
dialog.list = []  # type: ignore

# =з'єднання з чатом gpt через клас ChatGptService (gpt.py) та мій OPEN_AI_TOKEN
chatgpt = ChatGptService(  # type: ignore
    token="gpt:AU54YW8RRi4TXANWp060hfjiJxU6btLIvPmqxAgYF0QLgPDwmNfdLT5NyC9Y8r_u4QZeQmwhzFJFkblB3T4yhgCdA9W2KZIQwDchnwN-SRJKHph3pqraKQNsAmcDeSXdm_4aNY-8_3oiLFalGXckzNJlfA-T"
)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(CommandHandler("date", date))
app.add_handler(CommandHandler("message", message))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(date_button, "^date_.*"))
app.add_handler(CallbackQueryHandler(message_button, "^message_.*"))
app.run_polling()
