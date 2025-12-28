
# Telegram Multi-Platform Video Downloader Bot

A Telegram bot that allows users to download videos or audio from multiple social platforms (YouTube, TikTok, Instagram, Facebook, Twitter/X, Vimeo). Supports MP4 and MP3, quality selection, and multiple users concurrently.

## ✅ Features
- Download videos from YouTube, Instagram, TikTok, Facebook, Twitter/X, Vimeo
- YouTube MP4 (video) or MP3 (audio) selection
- Choose video quality for YouTube downloads
- Multi-user mode (isolated downloads per user)
- No file size or duration restrictions
- Automatic file cleanup

## 📦 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/ridhinva/telegram-video-downloader-bot.git
cd telegram-video-downloader-bot
```

### 2. Install dependencies
Ensure you have Python 3.9+ and `ffmpeg` installed.
```bash
pip install -r requirements.txt
```

Install `ffmpeg` (if not already installed):
```bash
# On Ubuntu/Debian:
sudo apt install ffmpeg

# On macOS (via Homebrew):
brew install ffmpeg
```

### 3. Set environment variable
Create a `.env` file or set the environment variable directly:
```bash
export TELEGRAM_BOT_TOKEN=your_bot_token_here
```

Alternatively, use a `.env` file:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### 4. Run the bot
```bash
python bot.py
```

## 📁 Project Structure
```
.
├── bot.py          # Main Telegram bot logic
├── config.py       # Configuration (token, formats, logging)
├── downloader.py   # Video/audio downloader logic
├── utils.py        # Utility helpers (URL parsing, cleaning)
├── README.md       # This file
```

## 💡 Usage
1. Send a supported video URL to the bot.
2. For YouTube:
   - Choose between MP4 (video) or MP3 (audio).
   - Select available quality.
3. Bot downloads and sends the file to your chat.

## 🛠 Built With
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- Python 3.9+

## 🔒 Privacy
- No personal user data is stored.
- All downloads are temporary and auto-deleted.

## 🧹 Cleanup
The bot automatically removes files after sending to keep the server clean.

## 🚀 Deployment Options

### 🔧 Deploy to Heroku
1. Install Heroku CLI and login.
2. Create a `Procfile`:
    ```
    worker: python bot.py
    ```
3. Push to Heroku:
    ```bash
    heroku create your-bot-name
    git push heroku main
    heroku config:set TELEGRAM_BOT_TOKEN=your_token_here
    heroku ps:scale worker=1
    ```

### 🐳 Docker Deployment
1. Create a `Dockerfile`:
    ```Dockerfile
    FROM python:3.9-slim

    WORKDIR /app
    COPY . /app

    RUN pip install --no-cache-dir -r requirements.txt

    CMD ["python", "bot.py"]
    ```

2. Build and run:
    ```bash
    docker build -t telegram-video-bot .
    docker run -e TELEGRAM_BOT_TOKEN=your_token_here telegram-video-bot
    ```

### ⚡ Railway Deployment
1. Create a new Railway project and link your GitHub repo.
2. Set environment variable `TELEGRAM_BOT_TOKEN`.
3. Use default build & run commands:
    ```
    Build: pip install -r requirements.txt
    Start: python bot.py
    ```

---

For all deployments, ensure `ffmpeg` is available (add it to Dockerfile or Railway Nixpacks if needed).

## 📬 Contact / Issues
Create an issue on the GitHub repo or contact the bot owner.

---

**License:** MIT
