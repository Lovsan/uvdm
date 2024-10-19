from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont
import yt_dlp
import time

class IntroThread(QThread):
    update_text = pyqtSignal(str)
    clear_text = pyqtSignal()

    def __init__(self, ascii_art, about_info):
        super().__init__()
        self.ascii_art = ascii_art
        self.about_info = about_info

    def run(self):
        # Typewriter effect for ASCII art
        for char in self.ascii_art:
            self.update_text.emit(char)
            time.sleep(0.02)
        time.sleep(0.5)
        # Typewriter effect for about info
        self.clear_text.emit()
        for char in self.about_info:
            self.update_text.emit(char)
            time.sleep(0.01)

class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        # ASCII art intro and about info
        self.ascii_art = r"""
  _    _  __     __ ____  __  __     
 | |  | | \ \   / /|  _ \|  \/  |    
 | |  | |  \ \ / / | | | | |\/| |    
 | |__| |   \ V /  | |_| | |  | |    
  \____/     \_/   |____/|_|  |_|    

  Ultimate Video Download Manager
"""
        self.about_info = r"""
Ultimate Video Download Manager (UVDM) is your one-stop solution for downloading and managing videos effortlessly.

Features:
- Download videos from popular websites with ease.
- Monitors clipboard for supported video links and prompts for download.
- Supports multiple video formats: MP3, MP4, AVI, and more.
- Single file downloads, playlist downloads, and batch downloads.
- Integrated download history with list view or grid view (with thumbnails), showing names, lengths, and sizes.
- Search downloaded files and play them in your default system player.
- Sorting and filtering options for downloaded content.
- Customizable themes for a personalized experience.
- Manage downloaded files directly within the app.
- Resume, rename, or delete downloads with a simple click.
- Choose video quality and format before downloading.
- Multi-threaded downloads for faster performance.
- View and manage active downloads.

Powered by yt-dlp, a powerful command-line tool for downloading videos from popular websites.

GitHub Repository:
- Ultimate Video Download Manager: https://github.com/username/uvdm
- yt-dlp: https://github.com/yt-dlp/yt-dlp

Enjoy a seamless video downloading experience!
"""

        # Label to display the intro text
        self.intro_label = QLabel()
        self.intro_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.intro_label)

        # Run typewriter effect in a separate QThread to avoid freezing UI
        self.intro_thread = IntroThread(self.ascii_art, self.about_info)
        self.intro_thread.update_text.connect(self.update_intro_text)
        self.intro_thread.clear_text.connect(self.clear_intro_text)
        self.intro_thread.start()

        # Add a button to view supported sites
        self.supported_sites_button = QPushButton("View Supported Sites")
        self.supported_sites_button.clicked.connect(self.open_supported_sites)
        self.layout.addWidget(self.supported_sites_button, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)

    def update_intro_text(self, char):
        current_text = self.intro_label.text() + char
        self.intro_label.setText(current_text)

    def clear_intro_text(self):
        self.intro_label.setText("")

    def open_supported_sites(self):
        # Create a new window to display supported sites
        self.supported_sites_window = QWidget()
        self.supported_sites_window.setWindowTitle("Supported Sites")
        layout = QVBoxLayout()

        # Correctly call list_extractors without arguments
        ie_list = yt_dlp.extractor.list_extractors()

        # Retrieve list of supported sites
        sites = sorted(set(ie.IE_NAME for ie in ie_list if ie.IE_NAME != 'generic'))

        # Create a QTextEdit to display the sites
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setText("\n".join(sites))
        layout.addWidget(text_edit)

        self.supported_sites_window.setLayout(layout)
        self.supported_sites_window.resize(400, 600)
        self.supported_sites_window.show()
