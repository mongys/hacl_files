import xml.etree.ElementTree as ET
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes
from telegram.ext.filters import TEXT, COMMAND

# Замените 'YOUR_TOKEN' на токен вашего бота
TELEGRAM_TOKEN = '6845607456:AAFQ2hlr3g71mjMMfuL5dLWnwajQJohclLw'

# Функция для чтения и поиска в XML-файле
def search_in_xml(query):
    tree = ET.parse('ГЭСНп.xml')
    root = tree.getroot()
    results = []

    for element in root.iter():
        if query.lower() in (element.get('Name', '').lower() or ''):
            results.append(element.get('Name'))
        if query.lower() in (element.get('EndName', '').lower() or ''):
            results.append(element.get('EndName'))
        if query.lower() in (element.get('Code', '').lower() or ''):
            results.append(element.get('Code'))

    return results

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Отправь мне сообщение, и я найду все совпадения в XML-файле.')

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.message.text
    results = search_in_xml(query)

    if results:
        response = "Найденные совпадения:\n" + "\n".join(results)
    else:
        response = "Совпадений не найдено."

    await update.message.reply_text(response)

def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(TEXT & ~COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()