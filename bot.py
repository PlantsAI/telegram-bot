import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, InlineQueryHandler
import config
from plantsai import PlantsAI


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)


async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_path = 'io/input/image.jpg'
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Image received. Processing...")
    file = await update.message.photo[-1].get_file()
    await file.download_to_drive(photo_path)
    class_names = plantsai(photo_path)
    calss_names = " ".join(class_names)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=calss_names)


if __name__ == '__main__':
    load_dotenv()
    Token = os.getenv("Token")
    application = ApplicationBuilder().token(Token).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    photo_handler = MessageHandler(filters.PHOTO, get_photo)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(inline_caps_handler)
    application.add_handler(photo_handler)

    plantsai = PlantsAI(weights_path=config.weights_path, image_size=config.image_size)

    application.run_polling()
