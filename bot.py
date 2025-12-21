# bot.py
"""
Telegram Video Downloader Bot (Enhanced)
"""
import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram.constants import ChatAction
from config import BOT_TOKEN, logger
from downloader import VideoDownloader
from utils import is_valid_url, get_platform_name

user_states = {}  # Stores user states and temporary choices
downloader = VideoDownloader()

class TelegramVideoBot:
    def __init__(self, token):
        self.token = token
        self.application = Application.builder().token(token).build()
        self.setup_handlers()

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            """
Welcome! Send me a video link (YouTube, Instagram, TikTok, etc).
For YouTube, I’ll ask if you want MP4 or MP3, and then show quality options.
            """,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Help", callback_data="help")]
            ])
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Just send a video link. For YouTube, you can choose format and quality.")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        url = update.message.text.strip()
        user_id = update.effective_user.id

        if not is_valid_url(url):
            await update.message.reply_text("❌ Invalid URL. Please send a video link.")
            return

        platform = get_platform_name(url)
        user_states[user_id] = {"url": url, "platform": platform}

        if platform == "YouTube":
            await update.message.reply_text(
                "Choose format:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🎞 MP4 (video)", callback_data="yt_mp4")],
                    [InlineKeyboardButton("🎵 MP3 (audio)", callback_data="yt_mp3")]
                ])
            )
        else:
            await self.process_download(update, context, user_id, url, audio_only=False)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        user_id = query.from_user.id
        await query.answer()

        if query.data == "help":
            await query.edit_message_text("Send me a video URL. I'll download it for you.")
            return

        if user_id not in user_states:
            await query.edit_message_text("Session expired. Please send the URL again.")
            return

        if query.data.startswith("yt_"):
            url = user_states[user_id]["url"]
            audio_only = query.data == "yt_mp3"
            formats = downloader.get_youtube_formats(url, audio_only)

            if not formats:
                await query.edit_message_text("Failed to retrieve quality options.")
                return

            buttons = [
                [InlineKeyboardButton(f"{fmt['format_note']} - {fmt['ext']}", callback_data=f"format_{fmt['format_id']}")]
                for fmt in formats
            ]
            user_states[user_id]["audio_only"] = audio_only
            user_states[user_id]["formats"] = formats
            await query.edit_message_text("Select quality:", reply_markup=InlineKeyboardMarkup(buttons))

        elif query.data.startswith("format_"):
            format_id = query.data.split("_", 1)[1]
            state = user_states[user_id]
            url = state["url"]
            audio_only = state["audio_only"]
            await query.edit_message_text("Downloading...")
            await self.process_download(update, context, user_id, url, audio_only, format_id)

    async def process_download(self, update, context, user_id, url, audio_only=False, format_id=None):
        try:
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_VIDEO)
            file_path, error = downloader.download_video(url, user_id, audio_only, format_id)

            if error:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"❌ Error: {error}")
                return

            with open(file_path, 'rb') as f:
                if audio_only:
                    await context.bot.send_audio(chat_id=update.effective_chat.id, audio=f)
                else:
                    await context.bot.send_video(chat_id=update.effective_chat.id, video=f, supports_streaming=True)

            os.remove(file_path)
            downloader.cleanup_user_files(user_id)
        except Exception as e:
            logger.error(str(e))
            await context.bot.send_message(chat_id=update.effective_chat.id, text="❌ Failed to send file.")

    def run(self):
        self.application.run_polling()

if __name__ == "__main__":
    bot = TelegramVideoBot(BOT_TOKEN)
    bot.run()
