import os
import requests
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QFileDialog, QMessageBox, QProgressBar, QDialog
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import yt_dlp
import json
import logging
from app.logger import YTDLPLogger

class BatchDownloadWorker(QObject):
    progress_updated = pyqtSignal(int)
    output_received = pyqtSignal(str)
    batch_download_finished = pyqtSignal()
    batch_download_failed = pyqtSignal(str)

    def __init__(self, urls, output_folder, settings_tab):
        super().__init__()
        self.urls = urls
        self.output_folder = output_folder
        self.settings_tab = settings_tab
        self.total_urls = len(urls)
        self.urls_downloaded = 0

    def run(self):
        try:
            for idx, url in enumerate(self.urls):
                self.download_single_video(url)
                self.urls_downloaded += 1
                progress = int((self.urls_downloaded / self.total_urls) * 100)
                self.progress_updated.emit(progress)
            self.batch_download_finished.emit()
        except Exception as e:
            self.batch_download_failed.emit(str(e))

    def download_single_video(self, url):
        try:
            ydl_opts = {
                'outtmpl': os.path.join(self.output_folder, '%(title)s.%(ext)s'),
                'format': 'best',
                'logger': YTDLPLogger(self.output_received),
                'progress_hooks': [self.my_hook],
                'quiet': True,
                'no_warnings': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            self.output_received.emit(f"Error downloading {url}: {e}")
            raise Exception(f"Failed to download {url}: {e}")

    def my_hook(self, d):
        if d['status'] == 'downloading':
            filename = d.get('filename', 'unknown')
            speed = d.get('_speed_str', '')
            eta = d.get('_eta_str', '')
            progress = d.get('_percent_str', '').strip()
            self.output_received.emit(f"{filename} - {progress} - Speed: {speed} - ETA: {eta}")
        elif d['status'] == 'finished':
            filename = d.get('filename', 'unknown')
            self.output_received.emit(f"Finished downloading {filename}")

class BatchDownloader(QWidget):
    def __init__(self, settings_tab):
        super().__init__()
        self.settings_tab = settings_tab
        self.layout = QVBoxLayout()

        self.label = QLabel("Batch Download Videos")

        # Editable text area for URLs
        self.url_text_edit = QTextEdit()
        self.url_text_edit.setPlaceholderText("Enter URLs here...")

        # Save and download buttons
        self.save_button = QPushButton("Save to TXT File")
        self.save_button.clicked.connect(self.save_to_txt)

        self.download_now_button = QPushButton("Download Now")
        self.download_now_button.clicked.connect(self.download_all_files)

        self.add_to_download_later_button = QPushButton("Add to Download Later")
        self.add_to_download_later_button.clicked.connect(self.add_to_download_later)

        # Layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.download_now_button)
        button_layout.addWidget(self.add_to_download_later_button)

        # Progress bar for download
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        # Add widgets to the layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.url_text_edit)
        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.progress_bar)
        self.setLayout(self.layout)

    def save_to_txt(self):
        """Save the URLs in the text area to a TXT file."""
        file_dialog = QFileDialog()
        txt_file_path, _ = file_dialog.getSaveFileName(self, "Save URLs to TXT File", "", "Text files (*.txt)")
        if txt_file_path:
            with open(txt_file_path, 'w') as file:
                file.write(self.url_text_edit.toPlainText())

    def add_to_download_later(self):
        """Add the URLs to the Download Later list."""
        urls = self.url_text_edit.toPlainText().splitlines()
        for url in urls:
            if url.strip():
                self.settings_tab.add_url_to_download_later(url)
        QMessageBox.information(self, "Added", "URLs added to Download Later.")

    def download_all_files(self):
        """Download the URLs in the text area."""
        urls = self.url_text_edit.toPlainText().splitlines()
        self.download_files(urls)

    def download_files(self, urls):
        """Start batch download in a new thread."""
        if not urls:
            QMessageBox.warning(self, "No URLs", "Please enter URLs to download.")
            return

        output_folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")

        if output_folder:
            self.thread = QThread()
            self.worker = BatchDownloadWorker(urls, output_folder, self.settings_tab)
            self.worker.moveToThread(self.thread)

            # Connect signals
            self.worker.progress_updated.connect(self.progress_bar.setValue)
            self.worker.output_received.connect(self.output_received)
            self.worker.batch_download_finished.connect(self.on_batch_download_complete)
            self.worker.batch_download_failed.connect(self.on_batch_download_failed)

            self.thread.started.connect(self.worker.run)
            self.thread.finished.connect(self.thread.deleteLater)

            self.thread.start()
        else:
            QMessageBox.warning(self, "Folder Selection", "Please select an output folder.")

    def output_received(self, text):
        # Handle output from the worker (e.g., print to console or log)
        print(text)

    def on_batch_download_complete(self):
        QMessageBox.information(self, "Batch Download Complete", "All videos downloaded successfully.")
        self.thread.quit()

    def on_batch_download_failed(self, error_message):
        QMessageBox.critical(self, "Batch Download Error", error_message)
        self.thread.quit()
