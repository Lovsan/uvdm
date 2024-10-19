import json
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox, QLineEdit, QHBoxLayout, QCheckBox
from app.themes import themes  # Ensure you have a themes.py file as shown below
from PyQt5.QtCore import Qt

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.default_view_label = QLabel("Default History View:")
        self.default_view_combo = QComboBox()
        self.default_view_combo.addItems(["List View", "Grid View"])

        self.quality_label = QLabel("Select Quality:")
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["Best", "High", "Medium", "Low"])

        self.format_label = QLabel("Select Format:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["MP4", "MP3", "AVI"])

        self.theme_label = QLabel("Select Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(list(themes.keys()))

        # Label for download playlist toggle
        self.playlist_checkbox = QCheckBox("Download Playlists (True/False)")
        self.playlist_checkbox.setChecked(True)  # Default to True
        self.playlist_checkbox.stateChanged.connect(self.update_playlist_state)

        # Label for download thumbnails toggle
        self.download_thumbnails_checkbox = QCheckBox("Download Thumbnails (True/False)")
        self.download_thumbnails_checkbox.setChecked(True)  # Default to True
        self.download_thumbnails_checkbox.stateChanged.connect(self.update_thumbnails_state)

        self.upload_settings_label = QLabel("Upload Settings:")
        self.upload_site_combo = QComboBox()
        self.upload_site_combo.addItems(["Select Site", "YouTube", "Vimeo", "Custom..."])
        self.upload_site_combo.currentIndexChanged.connect(self.check_custom_upload_site)

        self.custom_site_input = QLineEdit()
        self.custom_site_input.setPlaceholderText("Custom Upload Site URL")
        self.custom_site_input.setVisible(False)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username (if required)")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password (if required)")
        self.password_input.setEchoMode(QLineEdit.Password)

        # Layout for playlist and thumbnails options
        playlist_layout = QHBoxLayout()
        playlist_layout.addWidget(self.playlist_checkbox)
        thumbnail_layout = QHBoxLayout()
        thumbnail_layout.addWidget(self.download_thumbnails_checkbox)

        # Add to the main layout
        self.layout.addLayout(playlist_layout)
        self.layout.addLayout(thumbnail_layout)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)

        self.layout.addWidget(self.quality_label)
        self.layout.addWidget(self.quality_combo)
        self.layout.addWidget(self.format_label)
        self.layout.addWidget(self.format_combo)
        self.layout.addWidget(self.playlist_checkbox)
        self.layout.addWidget(self.download_thumbnails_checkbox)
        self.layout.addWidget(self.theme_label)
        self.layout.addWidget(self.theme_combo)
        self.layout.addWidget(self.upload_settings_label)
        self.layout.addWidget(self.upload_site_combo)
        self.layout.addWidget(self.custom_site_input)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.default_view_label)
        self.layout.addWidget(self.default_view_combo)

        self.setLayout(self.layout)

    def update_playlist_state(self, state):
        # Update the label to show True or False
        if state == Qt.Checked:
            self.playlist_checkbox.setText("Download Playlists (True)")
        else:
            self.playlist_checkbox.setText("Download Playlists (False)")

    def update_thumbnails_state(self, state):
        # Update the label to show True or False
        if state == Qt.Checked:
            self.download_thumbnails_checkbox.setText("Download Thumbnails (True)")
        else:
            self.download_thumbnails_checkbox.setText("Download Thumbnails (False)")
    
    def check_custom_upload_site(self, index):
        if self.upload_site_combo.currentText() == "Custom...":
            self.custom_site_input.setVisible(True)
        else:
            self.custom_site_input.setVisible(False)

    def save_settings(self):
        selected_theme = self.theme_combo.currentText()
        self.apply_theme(selected_theme)
        selected_quality = self.quality_combo.currentText()
        selected_format = self.format_combo.currentText()
        playlist_setting = self.playlist_checkbox.isChecked()
        download_thumbnails = self.download_thumbnails_checkbox.isChecked()
        upload_site = self.upload_site_combo.currentText()
        if upload_site == "Custom...":
            upload_site = self.custom_site_input.text()
        settings = {
            "quality": selected_quality,
            "format": selected_format,
            "theme": selected_theme,
            "download_playlists": playlist_setting,
            "download_thumbnails": download_thumbnails,
            "upload_site": upload_site,
            "username": self.username_input.text(),
            "password": self.password_input.text(),
            "default_history_view": self.default_view_combo.currentText(),
        }
        # Save settings to file
        if not os.path.exists('data'):
            os.makedirs('data')
        with open("data/settings.json", "w", encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
        QMessageBox.information(self, "Settings", "Settings applied successfully.")

    def apply_theme(self, theme_name):
        self.window().apply_theme(theme_name)

    def get_quality(self):
        return self.quality_combo.currentText()

    def get_format(self):
        return self.format_combo.currentText()

    def get_playlist_setting(self):
        return self.playlist_checkbox.isChecked()

    def get_upload_site(self):
        upload_site = self.upload_site_combo.currentText()
        if upload_site == "Custom...":
            return self.custom_site_input.text()
        else:
            return upload_site

    def get_upload_credentials(self):
        return {
            'username': self.username_input.text(),
            'password': self.password_input.text()
        }

    def add_url_to_download_later(self, url):
        json_file_path = os.path.join('data', 'download_later.json')
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                urls = json.load(f)
        else:
            urls = []
        if url not in urls:
            urls.append(url)
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(urls, f, indent=4)
