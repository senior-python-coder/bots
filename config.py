"""
Configuration settings for the Telegram Video Downloader Bot
"""
import os
import logging

# Bot configuration
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")

# Download settings
DOWNLOAD_DIR = "downloads"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB (Telegram limit)
SUPPORTED_PLATFORMS = [
    "youtube.com", "youtu.be", "instagram.com", "tiktok.com",
    "twitter.com", "x.com", "facebook.com", "vimeo.com"
]

# yt-dlp configuration
YT_DLP_OPTIONS = {
    'format': 'best[filesize<50M]/best',  # Prefer files under 50MB
    'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
    'extractaudio': False,
    'audioformat': 'mp3',
    'audioquality': '192K',
    'embed_subs': False,
    'writesubtitles': False,
    'writeautomaticsub': False,
    'ignoreerrors': True,
    'no_warnings': False,
    'extractflat': False,
    'writethumbnail': False,
    'writeinfojson': False,
}

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
