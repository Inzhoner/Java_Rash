from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *  # type: ignore
from util import *  # type: ignore

TOKEN = '7549253403:AAHuUvEdbWpsOkSqi4a-v9nZZgSK1cyJhS0'

#  + тут будемо писати наш код :)

async def start(update, context):
    msg = load_message('main')
    await  send_photo(update, context, 'main')
    await send_text(update, context, msg)
    await show_main_menu(update, context, {
        "start": "Головне меню",
        "profile": "Генерація Tinder-профіля \uD83D\uDD0E",
        "opener": "Повідомлення для знайомства \uD83D\uDCD7",
        "message": "Переписка від вашого імені \uD83D\uDCE8",
        "date": "Спілкування з зірками \uD83D\uDD25",
        "gpt": "Задати питання ChatGPT \uD83D\uDDE0",
    })


# =функція gpt - обробник на команду gpt
async def gpt(update, context):
    dialog.mode = 'gpt'
    await send_photo(update, context, 'gpt')
    msg = load_message('gpt')
    await send_text(update, context, msg)


# =функція оброблення повідомлення до чату gpt
async def gpt_dialog(update, context):
    text = update.message.text
    promt = load_prompt('gpt')
    answer = await chatgpt.send_question(promt, text)
    await send_text(update, context, answer)


# =функція hello - відповідає на введення будь-якого тексту у боті
async def hello(update, context):
    if dialog.mode == 'gpt':
        await gpt_dialog(update, context)

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

# =з'єднання з чатом gpt через клас ChatGptService (gpt.py) та мій OPEN_AI_TOKEN
chatgpt = ChatGptService(  # type: ignore
    token='gpt:AU54YW8RRi4TXANWp060hfjiJxU6btLIvPmqxAgYF0QLgPDwmNfdLT5NyC9Y8r_u4QZeQmwhzFJFkblB3T4yhgCdA9W2KZIQwDchnwN-SRJKHph3pqraKQNsAmcDeSXdm_4aNY-8_3oiLFalGXckzNJlfA-T')

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('gpt', gpt))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
# app.add_handler(CallbackQueryHandler(buttons_handler))
app.run_polling()
