from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters, CommandHandler
from rag import answer_question
import asyncio 
from telegram.constants import ChatAction



load_dotenv()
BOT_TOKEN=os.getenv('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привіт! Постав мені питання по базі знань.')

async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    await update.message.chat.send_action(ChatAction.TYPING)
    result = await asyncio.to_thread(answer_question, question)

    text = result['answer']
    if result['sources']:
        text += '\n\nsources:\n' + '\n'.join(result['sources'])
    text = text[:4096]

    await update.message.reply_text(text)

app = ApplicationBuilder().token(token=BOT_TOKEN).connect_timeout(30).read_timeout(30).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_question))


app.run_polling()