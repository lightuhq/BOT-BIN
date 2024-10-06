from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import requests
import logging
import asyncio

TOKEN = '7244633347:AAH6sHCo-0mHBCxU-G6S5ji5rItL9pQTKcQ'
API_KEY = 'cd1f2672beec9ac7574ef83b89533c63929d3512'
API_URL = 'https://api.bintable.com/v1/'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def escape_markdown_v2(text: str) -> str:
    special_chars = [
        '.', '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '!'
    ]
    for char in special_chars:
        text = text.replace(char, '\\' + char)
    return text

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('/𝙗𝙞𝙣 𝙥𝙤𝙪𝙧 𝙪𝙩𝙞𝙡𝙞𝙨𝙚𝙧 𝙡𝙚 𝙗𝙤𝙩.')

async def bin(update: Update, context: CallbackContext) -> None:
    bin_number = ' '.join(context.args)
    if not bin_number:
        msg = await update.message.reply_text("Faut mettre un bin sale merde !")
        await asyncio.sleep(15)
        await update.message.delete()
        return

    try:
        await update.message.reply_text("🔍 𝙏𝙧𝙖𝙞𝙩𝙚𝙢𝙚𝙣𝙩 𝙚𝙣 𝙘𝙤𝙪𝙧𝙨...")
        response = requests.get(f"{API_URL}{bin_number}?api_key={API_KEY}")
        data = response.json()

        if data.get('result') == 404:
            await update.message.reply_text("🚫 Bin invalide !")
        else:
            card_data = data['data']['card']
            country_data = data['data']['country']
            bank_data = data['data']['bank']

            text = (
                f"🔎 𝐁𝐈𝐍: {bin_number}\n"
                f"🏦 𝐁𝐀𝐍𝐐𝐔𝐄: {bank_data.get('name', 'N/A')}\n"
                f"💳 𝐓𝐘𝐏𝐄 𝐃𝐄 𝐂𝐀𝐑𝐓𝐄: {card_data.get('type', 'N/A')}\n"
                f"💳 𝐌𝐀𝐑𝐐𝐔𝐄: {card_data.get('scheme', 'N/A')}\n"
                f"💳 𝐂𝐀𝐓𝐄𝐆𝐎𝐑𝐈𝐄: {card_data.get('category', 'N/A')}\n"
                f"🌍 𝐏𝐀𝐘𝐒: {country_data.get('name', 'N/A')}\n"
            )

            escaped_text = escape_markdown_v2(text)
            await update.message.reply_text(escaped_text, parse_mode='MarkdownV2')

    except Exception as e:
        error_message = f"**Oops Error!**\n{escape_markdown_v2(str(e))}\n\n**Y'a eu un bug frérot !**"
        await update.message.reply_text(error_message, parse_mode='MarkdownV2')

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('bin', bin))
    application.run_polling()

if __name__ == '__main__':
    main()
