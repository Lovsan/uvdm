# upload_form_widget.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QComboBox, QProgressBar, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import os
import requests
from app.upload_worker_new import UploadWorker

class UploadFormWidget(QWidget):
    upload_successful = pyqtSignal(dict)
    upload_failed = pyqtSignal(str)

    def __init__(self, video_path, available_sites):
        super().__init__()
        self.video_path = video_path
        self.available_sites = available_sites
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Upload Video")
        self.layout = QVBoxLayout()

        # Site selection
        self.site_label = QLabel("Select Upload Site:")
        self.site_combo = QComboBox()
        self.site_combo.addItems(self.available_sites.keys())

        # API Key
        self.api_key_label = QLabel("API Key:")
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter your API key")

        # File Path (Read-only, since the file is pre-selected)
        self.file_label = QLabel("File to Upload:")
        self.file_path_label = QLabel(self.video_path)
        self.file_path_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # Upload Button
        self.upload_button = QPushButton("Upload")
        self.upload_button.clicked.connect(self.start_upload)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)

        # Result Display
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True) #
        self.result_display.setVisible(True) # 

        # Layout arrangement
        self.layout.addWidget(self.site_label)
        self.layout.addWidget(self.site_combo)
        self.layout.addWidget(self.api_key_label)
        self.layout.addWidget(self.api_key_input)
        self.layout.addWidget(self.file_label)
        self.layout.addWidget(self.file_path_label)
        self.layout.addWidget(self.upload_button)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.result_display)

        self.setLayout(self.layout)
        self.resize(400, 300)

    def start_upload(self):
        api_key = self.api_key_input.text().strip()
        if not api_key:
            QMessageBox.warning(self, "API Key Required", "Please enter your API key.")
            return

        selected_site = self.site_combo.currentText()
        upload_url = self.available_sites[selected_site]

        self.upload_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.result_display.setVisible(False)

        self.upload_thread = QThread()
        self.upload_worker = UploadWorker(self.video_path, api_key, upload_url)
        self.upload_worker.moveToThread(self.upload_thread)

        self.upload_worker.upload_progress.connect(self.update_progress)
        self.upload_worker.upload_finished.connect(self.upload_success)
        self.upload_worker.upload_failed.connect(self.upload_failure)

        self.upload_thread.started.connect(self.upload_worker.run)
        self.upload_thread.finished.connect(self.upload_thread.deleteLater)

        self.upload_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def upload_success(self, result):
        self.upload_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.result_display.setVisible(True)
        self.result_display.setText(f"Upload Successful!\nResponse:\n{result}")
        self.upload_thread.quit()
        self.upload_successful.emit(result)

    def upload_failure(self, error_message):
        self.upload_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.result_display.setVisible(True)
        self.result_display.setText(f"Upload Failed:\n{error_message}")
        self.upload_thread.quit()
        self.upload_failed.emit(error_message)
