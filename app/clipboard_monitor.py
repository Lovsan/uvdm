import time
import re
from PyQt5.QtCore import QThread, pyqtSignal
import pyperclip

class ClipboardMonitor(QThread):
    """Monitors the clipboard for video URLs."""
    new_url_found = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.recent_value = ""

    def run(self):
        while True:
            clipboard_content = pyperclip.paste()
            if clipboard_content != self.recent_value and self.is_video_url(clipboard_content):
                self.recent_value = clipboard_content
                self.new_url_found.emit(clipboard_content)
            time.sleep(2)  # Check every 2 seconds

    def is_video_url(self, text):
        """Check if the clipboard text is a video URL."""
        video_sites = [
            'youtube', 'youtu', 'vimeo', 'facebook', 'fb', 'dailymotion', 'twitch',
            'twitter', 'instagram', 'tiktok', 'reddit', 'liveleak', 'metacafe', 'veoh',
            'break', '9gag', 'vid.me', 'redgifs', 'periscope', 'streamable', 'archive.org'
        ]
        pattern = r'(https?://(www\.)?(' + '|'.join(video_sites) + r')[^\s]+)'
        return re.search(pattern, text)
