"""
Video downloader module using yt-dlp
"""
import os
import tempfile
import logging
import yt_dlp
from config import YT_DLP_OPTIONS, MAX_FILE_SIZE, DOWNLOAD_DIR
from utils import ensure_download_dir, sanitize_filename

logger = logging.getLogger(__name__)

class VideoDownloader:
    def __init__(self):
        self.download_dir = DOWNLOAD_DIR
        ensure_download_dir()
    
    def download_video(self, url, user_id=None):
        """
        Download video from URL and return file path
        """
        try:
            # Create user-specific temporary directory
            temp_dir = os.path.join(self.download_dir, f"user_{user_id}" if user_id else "temp")
            os.makedirs(temp_dir, exist_ok=True)
            
            # Configure yt-dlp options with custom output template
            options = YT_DLP_OPTIONS.copy()
            options['outtmpl'] = os.path.join(temp_dir, '%(title)s.%(ext)s')
            
            with yt_dlp.YoutubeDL(options) as ydl:
                # Extract info first to check file size
                try:
                    info = ydl.extract_info(url, download=False)
                    if not info:
                        return None, "Could not extract video information"
                    
                    # Check if video duration is reasonable (max 10 minutes)
                    duration = info.get('duration', 0)
                    if duration and duration > 600:  # 10 minutes
                        return None, "Video is too long (max 10 minutes allowed)"
                    
                    # Check estimated file size
                    filesize = info.get('filesize') or info.get('filesize_approx', 0)
                    if filesize and filesize > MAX_FILE_SIZE:
                        return None, f"Video file is too large (max 50MB allowed)"
                    
                    # Get video title for filename
                    title = info.get('title', 'video')
                    title = sanitize_filename(title)
                    
                except Exception as e:
                    logger.error(f"Error extracting info for {url}: {e}")
                    return None, f"Error processing video: {str(e)}"
                
                # Download the video
                try:
                    ydl.download([url])
                    
                    # Find the downloaded file
                    downloaded_file = None
                    for file in os.listdir(temp_dir):
                        if file.endswith(('.mp4', '.mkv', '.webm', '.avi', '.mov', '.flv')):
                            downloaded_file = os.path.join(temp_dir, file)
                            break
                    
                    if not downloaded_file or not os.path.exists(downloaded_file):
                        return None, "Download completed but file not found"
                    
                    # Check actual file size
                    actual_size = os.path.getsize(downloaded_file)
                    if actual_size > MAX_FILE_SIZE:
                        os.remove(downloaded_file)
                        return None, f"Downloaded file is too large ({actual_size / 1024 / 1024:.1f}MB)"
                    
                    logger.info(f"Successfully downloaded: {downloaded_file} ({actual_size / 1024 / 1024:.1f}MB)")
                    return downloaded_file, None
                    
                except Exception as e:
                    logger.error(f"Error downloading {url}: {e}")
                    return None, f"Download failed: {str(e)}"
                    
        except Exception as e:
            logger.error(f"Unexpected error downloading {url}: {e}")
            return None, f"Unexpected error: {str(e)}"
    
    def get_video_info(self, url):
        """
        Get video information without downloading
        """
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    return {
                        'title': info.get('title', 'Unknown'),
                        'duration': info.get('duration', 0),
                        'uploader': info.get('uploader', 'Unknown'),
                        'view_count': info.get('view_count', 0),
                        'upload_date': info.get('upload_date', 'Unknown')
                    }
        except Exception as e:
            logger.error(f"Error getting info for {url}: {e}")
        
        return None
    
    def cleanup_user_files(self, user_id):
        """
        Clean up all files for a specific user
        """
        try:
            user_dir = os.path.join(self.download_dir, f"user_{user_id}")
            if os.path.exists(user_dir):
                for file in os.listdir(user_dir):
                    file_path = os.path.join(user_dir, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                os.rmdir(user_dir)
                logger.info(f"Cleaned up files for user {user_id}")
        except Exception as e:
            logger.error(f"Error cleaning up files for user {user_id}: {e}")
