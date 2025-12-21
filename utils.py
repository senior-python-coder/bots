"""
Utility functions for the Telegram Video Downloader Bot
"""
import re
import os
import tempfile
import logging
from urllib.parse import urlparse
from config import SUPPORTED_PLATFORMS, DOWNLOAD_DIR

logger = logging.getLogger(__name__)

def is_valid_url(url):
    """
    Validate if the provided URL is a valid video URL from supported platforms
    """
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return False
        
        domain = parsed.netloc.lower()
        # Remove www. prefix if present
        if domain.startswith('www.'):
            domain = domain[4:]
        
        # Check if domain is in supported platforms
        for platform in SUPPORTED_PLATFORMS:
            if domain in platform or platform in domain:
                return True
        
        return False
    except Exception as e:
        logger.error(f"Error validating URL {url}: {e}")
        return False

def get_platform_name(url):
    """
    Extract platform name from URL
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if domain.startswith('www.'):
            domain = domain[4:]
        
        if 'youtube.com' in domain or 'youtu.be' in domain:
            return "YouTube"
        elif 'instagram.com' in domain:
            return "Instagram"
        elif 'tiktok.com' in domain:
            return "TikTok"
        elif 'twitter.com' in domain or 'x.com' in domain:
            return "Twitter/X"
        elif 'facebook.com' in domain:
            return "Facebook"
        elif 'vimeo.com' in domain:
            return "Vimeo"
        else:
            return "Unknown"
    except:
        return "Unknown"

def ensure_download_dir():
    """
    Ensure download directory exists
    """
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
        logger.info(f"Created download directory: {DOWNLOAD_DIR}")

def cleanup_file(file_path):
    """
    Clean up downloaded file
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Cleaned up file: {file_path}")
    except Exception as e:
        logger.error(f"Error cleaning up file {file_path}: {e}")

def get_file_size(file_path):
    """
    Get file size in bytes
    """
    try:
        return os.path.getsize(file_path)
    except:
        return 0

def format_file_size(size_bytes):
    """
    Format file size in human readable format
    """
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def sanitize_filename(filename):
    """
    Sanitize filename for safe storage
    """
    # Remove invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    if len(filename) > 100:
        name, ext = os.path.splitext(filename)
        filename = name[:95] + ext
    
    return filename
