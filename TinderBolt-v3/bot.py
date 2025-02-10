from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *  # type: ignore
from util import *  # type: ignore

TOKEN = '7549253403:AAHuUvEdbWpsOkSqi4a-v9nZZgSK1cyJhS0'


#  + тут будемо писати наш код :)
async def start(update, context):
    # await send_photo(update, context, 'avatar_main')
    # await send_text(update, context, "Привіт користувач!")
    msg = load_message('main')
    await send_text(update, context, msg)


async def hello(update, context):
    # await send_text(update, context, "Hello  " + update.message.text)
    await send_text_buttons(update, context, "Hello  " + update.message.text, {
        'start': 'START',
        'stop': 'STOP'
    })


async def buttons_handler(update, context):
    query = update.callback_query.data
    if query == 'start':
        await send_text(update, context, 'Started!')
    elif query == 'stop':
        await send_text(update, context, 'Stopped!')


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(buttons_handler))
app.run_polling()
