import logging
import yaml
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, Application, filters, MessageHandler
from io import BytesIO
from image_processor import main_pipeline, save_colors



NUM_COLORS = 8
TRUNC_VAL = 40
BLUR_RADIUS = 10
PALETTE_SHAPE = (4, 2, 3)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='BOT IS RUNNING')


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Echo bot\n'
                                                                          'Бот возвращает написанное ему сообщение\n'
                                                                          'Использование:\n'
                                                                          '/start\n'
                                                                          '/help\n'
                                                                          'ответ на сообщение бота\n'
                                                                          f'@{context.bot.bot.username}')


async def echo_mention(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(text=f'Пошёл нахуй, @{update.effective_message.from_user.username}', do_quote=True)


async def echo_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.reply_to_message:
        if update.effective_message.reply_to_message.from_user.username == f'{context.bot.bot.username}':
            await update.effective_message.reply_text(text=update.effective_message.text, do_quote=True)


async def get_colors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    avatars = await update.effective_message.from_user.get_profile_photos()
    first_ava_file = await avatars.photos[0][2].get_file()
    ava_buffer = BytesIO()
    with ava_buffer:
        await first_ava_file.download_to_memory(ava_buffer)
        top_n_colors = main_pipeline(ava_buffer, NUM_COLORS, TRUNC_VAL, BLUR_RADIUS)
    colors_buffer = BytesIO()
    with colors_buffer:
        save_colors(top_n_colors, colors_buffer, PALETTE_SHAPE)
        await update.effective_message.reply_photo(colors_buffer.getvalue())



if __name__ == "__main__":
    with open('conf.yaml') as conf_file:
        conf = yaml.safe_load(conf_file)
        api_token = conf['API_TOKEN']
        username = conf['USERNAME']
    app = ApplicationBuilder().token(api_token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(CommandHandler('get_colors', get_colors))
    app.add_handler(MessageHandler(filters.Mention(f'@{username}'), echo_mention))
    app.add_handler(MessageHandler(filters.ALL, echo_reply))
    app.run_polling(allowed_updates=Update.ALL_TYPES)
