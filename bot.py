import os

from telegram import Update, ForceReply
from telegram.ext import CommandHandler, CallbackContext, ApplicationBuilder, ConversationHandler, filters, \
    MessageHandler

from dotenv import load_dotenv

from api_hendler import DataParser

load_dotenv()

WAITING_FOR_ADDRESS: str = ''


class BscScanBot:
    def __init__(self):
        self.application = ApplicationBuilder().token(os.environ.get("TELE_TOKEN")).build()
        self.setup_handlers()

    async def start(self, update: Update, context: CallbackContext) -> str:
        await update.message.reply_text('Hello! I am here to show you your transaction history on "BscScan".')
        await update.message.reply_text(
            'Enter the address.',
            reply_markup=ForceReply(selective=False)
        )
        return WAITING_FOR_ADDRESS

    async def get_address(self, update: Update, context: CallbackContext):
        address = update.message.text
        if not address.startswith("0x") or not address:
            await update.message.reply_text("Incorrect address, the bot has stopped, please press /start again")
            return ConversationHandler.END
        data = DataParser(address)
        result = data.get_info()
        if isinstance(result, str):
            await update.message.reply_text(f"{result}")
            return ConversationHandler.END
        await self.send_large_list(update.message.chat_id, result, context.bot)
        return ConversationHandler.END

    @staticmethod
    async def send_large_list(chat_id, large_list, tele_bot):
        chunk_size = 5
        for i in range(0, len(large_list), chunk_size):
            chunk = large_list[i:i + chunk_size]
            message_text = '\n'.join(str(item) + "\n" for item in chunk)
            await tele_bot.send_message(chat_id=chat_id, text=message_text)

    def setup_handlers(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                WAITING_FOR_ADDRESS: [MessageHandler(filters.TEXT & (~filters.COMMAND), self.get_address)],
            },
            fallbacks=[]
        )
        self.application.add_handler(conv_handler)

    def run(self):
        self.application.run_polling()


if __name__ == '__main__':
    bot = BscScanBot()
    bot.run()
