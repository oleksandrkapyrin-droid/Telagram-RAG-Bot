from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters



load_dotenv()
BOT_TOKEN=os.getenv('BOT_TOKEN')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

app = ApplicationBuilder().token(token=BOT_TOKEN).connect_timeout(30).read_timeout(30).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


app.run_polling()