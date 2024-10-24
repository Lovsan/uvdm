import os
import platform
import subprocess
import time
import requests
import re
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QProgressBar, QMessageBox, QTextEdit
)
from PyQt5.QtCore import QThread
from app.download_worker import DownloadWorker
from app.upload_worker import UploadWorker
from app.batch_downloader import BatchDownloader

class YTDLPTab(QWidget):
    def __init__(self, settings_tab, download_manager, history_tab, tab_index, tab_widget, download_later_tab):
        super().__init__()
        self.settings_tab = settings_tab
        self.batch_downloader = BatchDownloader(self.settings_tab)
        self.download_manager = download_manager
        self.history_tab = history_tab
        self.download_later_tab = download_later_tab
        self.tab_index = tab_index
        self.tab_widget = tab_widget
        self.layout = QVBoxLayout()

        # [Input] section - Top half
        self.url_label = QLabel("Enter URL:")
        self.url_input = QLineEdit()
        self.cmd_output = QTextEdit()
        self.cmd_output.setReadOnly(True)
        self.cmd_output.setFixedHeight(200)

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.start_download_thread)
        self.output_folder_label = QLabel("Output Folder:")
        self.output_folder_button = QPushButton("Select Folder")
        self.output_folder_button.clicked.connect(self.set_output_folder)
        self.output_file_name_input = QLineEdit()
        self.output_file_name_input.setPlaceholderText("Select Filename")
        self.output_folder = os.path.join(os.getcwd(), "Downloads")

        self.layout.addWidget(self.url_label)
        self.layout.addWidget(self.url_input)
        self.layout.addWidget(self.cmd_output)
        self.layout.addWidget(self.output_folder_label)
        self.layout.addWidget(self.output_folder_button)
        self.layout.addWidget(self.output_file_name_input)
        self.layout.addWidget(self.download_button)

        self.video_title_label = QLabel("Title: ")
        self.video_path_label = QLabel("Path: ")
        self.output_file_name_label = QLabel("Filename: ")
        self.video_size_label = QLabel("Size: ")
        self.download_duration_label = QLabel("Download Duration: ")
        self.play_button = QPushButton("Play Video")
        self.play_button.setEnabled(False)
        self.play_button.clicked.connect(self.play_video)

        self.upload_button = QPushButton("Upload Video")
        self.upload_button.setEnabled(False)
        self.upload_button.clicked.connect(self.upload_video)

        self.layout.addWidget(self.video_title_label)
        self.layout.addWidget(self.video_path_label)
        self.layout.addWidget(self.download_duration_label)
        self.layout.addWidget(self.video_size_label)
        self.layout.addWidget(self.play_button)
        self.setLayout(self.layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

        self.downloaded_video_path = None

    def set_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder:
            self.output_folder = folder

    def start_download_thread(self):
        url = self.url_input.text()
        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a valid URL.")
            return

        self.update_tab_title("Downloading...")

        self.thread = QThread()
        self.worker = DownloadWorker(url, self.output_folder, self.settings_tab)
        self.worker.moveToThread(self.thread)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.download_finished.connect(self.on_download_complete)
        self.worker.download_failed.connect(self.handle_error)
        self.worker.title_found.connect(self.update_tab_title)
        self.worker.output_received.connect(self.update_cmd_output)
        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.thread.deleteLater)

        self.start_time = time.time()
        self.thread.start()

    def update_cmd_output(self, output_text):
        """Update the command line output (cmd) section with real-time info."""
        self.cmd_output.append(output_text)

    def handle_error(self, url, error_message):
        """Handle errors emitted by the worker."""
        QMessageBox.critical(self, "Download Error", f"Error downloading {url}:\n{error_message}")
        self.thread.quit()

    def update_progress(self, value):
        """Update the progress bar and show the percentage in the window."""
        self.progress_bar.setValue(value)
        self.progress_bar.setFormat(f"Downloading: {value}%")

    def update_tab_title(self, title):
        """Update the tab title when the video title is found."""
        self.tab_widget.setTabText(self.tab_index, title)

    def on_download_complete(self, video_title, video_path):
        duration = time.time() - self.start_time
        self.video_title_label.setText(f"Title: {video_title}")
        self.video_path_label.setText(f"Path: {video_path}")
        self.download_duration_label.setText(f"Download Duration: {duration:.2f} seconds")
        self.downloaded_video_path = video_path
        self.play_button.setEnabled(True)
        self.upload_button.setEnabled(True)

        # Refresh download history
        self.history_tab.load_downloads_history()

        # If the URL was in the Download Later list, remove it
        self.download_later_tab.remove_url(self.url_input.text())

        # Update download queue label
        self.download_manager.update_download_queue_label()

    def play_video(self):
        if self.downloaded_video_path and os.path.exists(self.downloaded_video_path):
            system = platform.system().lower()

            try:
                if system == "windows":
                    os.startfile(self.downloaded_video_path)
                elif system == "darwin":  # macOS
                    subprocess.call(["open", self.downloaded_video_path])
                elif system == "linux":
                    subprocess.call(["xdg-open", self.downloaded_video_path])
                else:
                    QMessageBox.warning(self, "Unsupported OS",
                                        "Video playback is not supported on this operating system.")
            except Exception as e:
                QMessageBox.warning(self, "Playback Error",
                                    f"An error occurred while trying to play the video: {str(e)}")
        else:
            QMessageBox.warning(self, "File Error", "The video file could not be found.")
    def upload_video(self):
        upload_site = self.settings_tab.get_upload_site()
        if not upload_site:
            QMessageBox.warning(self, "Upload Error", "No upload site configured in settings.")
            return

        self.upload_thread = QThread()
        self.upload_worker = UploadWorker(self.downloaded_video_path, upload_site, self.settings_tab)
        self.upload_worker.moveToThread(self.upload_thread)

        self.upload_worker.upload_finished.connect(self.on_upload_complete)
        self.upload_worker.upload_failed.connect(self.on_upload_failed)
        self.upload_thread.started.connect(self.upload_worker.run)
        self.upload_thread.finished.connect(self.upload_thread.deleteLater)

        self.upload_thread.start()

    def on_upload_complete(self, upload_info):
        QMessageBox.information(self, "Upload Complete", f"Video uploaded successfully to {upload_info['site']}.")
        self.upload_button.setEnabled(False)
        # Add to uploads history
        self.download_manager.uploads_tab.add_upload_entry(upload_info)

    def on_upload_failed(self, error_message):
        QMessageBox.critical(self, "Upload Failed", error_message)
