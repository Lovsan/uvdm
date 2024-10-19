import os
import time
import requests
import re
import json
import logging
import traceback
from PyQt5.QtCore import QObject, pyqtSignal
import yt_dlp
from app.logger import YTDLPLogger

class DownloadWorker(QObject):
    progress_updated = pyqtSignal(int)
    download_finished = pyqtSignal(str, str)
    download_failed = pyqtSignal(str, str)
    title_found = pyqtSignal(str)
    output_received = pyqtSignal(str)

    def __init__(self, url, output_folder, settings_tab, parent=None):
        super().__init__(parent)
        self.url = url
        self.output_folder = output_folder
        self.settings_tab = settings_tab
        self.total_videos = 1
        self.videos_downloaded = 0
        self.playlist_title = "Downloading..."

    def extract_source_site(self, url):
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        return parsed_url.netloc.replace('www.', '')

    def save_video_info(self, video_info, json_file_path):
        """Save the video information to a JSON file."""
        try:
            if os.path.exists(json_file_path):
                with open(json_file_path, "r", encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = []

            data.append(video_info)

            with open(json_file_path, "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        except Exception as e:
            logging.error(f"Error in save_video_info: {e}")

    def run(self):
        try:
            # Create an instance of YTDLPLogger
            self.logger = YTDLPLogger()
            # Connect the logger's output_signal to the worker's output_received signal
            self.logger.output_signal.connect(self.output_received)

            initial_opts = {
                "format": "best",
                "outtmpl": os.path.join(self.output_folder, "%(title)s.%(ext)s"),
                "noplaylist": not self.settings_tab.get_playlist_setting(),
                'logger': self.logger,
                'progress_hooks': [self.my_hook],
                'quiet': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(initial_opts) as ydl:
                # Extract info to get playlist details
                info = ydl.extract_info(self.url, download=False)

            if 'entries' in info and isinstance(info['entries'], list):
                self.playlist_title = info.get('title', 'Playlist')
                self.total_videos = len(info['entries'])
                # Sanitize playlist title for folder name
                playlist_folder = re.sub(r'[\\/*?:"<>|]', "_", self.playlist_title)
                output_path = os.path.join(self.output_folder, playlist_folder, "%(title)s.%(ext)s")
            else:
                self.playlist_title = info.get('title', 'Video')
                self.total_videos = 1
                # Single video, no folder creation
                output_path = os.path.join(self.output_folder, "%(title)s.%(ext)s")

            # Update ydl_opts with the correct outtmpl
            ydl_opts = {
                "format": "best",
                "outtmpl": output_path,
                "noplaylist": not self.settings_tab.get_playlist_setting(),
                'logger': self.logger,
                'progress_hooks': [self.my_hook],
                'quiet': True,
                'no_warnings': True,
            }

            self.title_found.emit(f"{self.playlist_title} (0/{self.total_videos})")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])

        except yt_dlp.utils.DownloadError as e:
            logging.error(f"Download error: {e}\n{traceback.format_exc()}")
            self.download_failed.emit(self.url, str(e))
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}\n{traceback.format_exc()}")
            self.download_failed.emit(self.url, str(e))

    def my_hook(self, d):
        try:
            if d['status'] == 'downloading':
                percentage = d.get('_percent_str', '0%').strip().replace('%', '')
                try:
                    percentage = float(percentage)
                    self.progress_updated.emit(int(percentage))
                except ValueError:
                    pass  # Ignore if percentage can't be converted
            elif d['status'] == 'finished':
                self.videos_downloaded += 1
                self.progress_updated.emit(100)
                time.sleep(0.5)  # Small delay to ensure the progress bar shows 100%
                # Update tab title with progress
                self.title_found.emit(f"{self.playlist_title} ({self.videos_downloaded}/{self.total_videos})")

                # Get video info
                info = d.get('info_dict', {})
                if not isinstance(info, dict):
                    logging.error(f"Expected 'info_dict' to be a dict, got {type(info)}")
                    return
                file_path = d.get('filename', '')

                video_info = {
                    "title": info.get("title", "Unknown Title"),
                    "path": file_path,
                    "size": info.get("filesize") or info.get("filesize_approx"),
                    "url": info.get("webpage_url", ""),
                    "duration": info.get("duration", 0),
                    "thumbnail": "",
                    "source_site": self.extract_source_site(info.get("webpage_url", ""))
                }

                # Download thumbnail if the option is enabled in settings
                if self.settings_tab.download_thumbnails_checkbox.isChecked():
                    thumbnail_url = info.get("thumbnail", "")
                    if thumbnail_url:
                        try:
                            response = requests.get(thumbnail_url, stream=True)
                            response.raise_for_status()

                            # Extract video title for thumbnail filename
                            video_title = re.sub(r'[\\/*?:"<>|]', "_", info.get("title", "unknown"))
                            thumbnail_path = os.path.join("data", "thumbnails", f"{video_title}.jpg")
                            if not os.path.exists(os.path.dirname(thumbnail_path)):
                                os.makedirs(os.path.dirname(thumbnail_path))
                            with open(thumbnail_path, "wb") as f:
                                for chunk in response.iter_content(chunk_size=8192):
                                    f.write(chunk)
                            # Update the video_info with the downloaded thumbnail path
                            video_info["thumbnail"] = thumbnail_path
                        except requests.exceptions.RequestException as e:
                            logging.error(f"Error downloading thumbnail: {e}")

                self.save_video_info(video_info, os.path.join("data", "downloads.json"))

                # If all videos are downloaded, emit download_finished signal
                if self.videos_downloaded == self.total_videos:
                    self.download_finished.emit(self.playlist_title, file_path)
        except Exception as e:
            logging.error(f"Error in my_hook: {e}\n{traceback.format_exc()}")
