import json
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QLabel, QComboBox, QPushButton, QMessageBox,
    QLineEdit, QHBoxLayout, QCheckBox, QFormLayout, QSlider, QFileDialog, QGroupBox
)
from PyQt5.QtCore import Qt

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout for the settings page
        main_layout = QVBoxLayout()

        # Create a QTabWidget to hold the different sections
        self.tabs = QTabWidget()
        self.main_settings_tab = QWidget()
        self.styles_tab = QWidget()
        self.upload_settings_tab = QWidget()
        self.download_settings_tab = QWidget()
        self.proxy_settings_tab = QWidget()

        # Add tabs to the QTabWidget
        self.tabs.addTab(self.main_settings_tab, "Main Settings")
        self.tabs.addTab(self.styles_tab, "Styles")
        self.tabs.addTab(self.upload_settings_tab, "Upload Settings")
        self.tabs.addTab(self.download_settings_tab, "Download Settings")
        self.tabs.addTab(self.proxy_settings_tab, "Proxy Settings")

        # Populate each tab with settings
        self.setup_main_settings()
        self.setup_styles_settings()
        self.setup_upload_settings()
        self.setup_download_settings()
        self.setup_proxy_settings()

        # Add the tabs to the main layout
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def setup_main_settings(self):
        layout = QVBoxLayout()

        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter your API key")
        layout.addWidget(QLabel("API Key:"))
        layout.addWidget(self.api_key_input)

        self.default_view_label = QLabel("Default History View:")
        self.default_view_combo = QComboBox()
        self.default_view_combo.addItems(["List View", "Grid View"])
        layout.addWidget(self.default_view_label)
        layout.addWidget(self.default_view_combo)

        self.main_settings_tab.setLayout(layout)

    def setup_styles_settings(self):
        layout = QFormLayout()

        # List available themes
        self.theme_combo = QComboBox()
        theme_folder = os.path.join(os.getcwd(), 'themes')
        if os.path.exists(theme_folder):
            themes = [f.replace('.py', '') for f in os.listdir(theme_folder) if f.endswith('.py')]
            self.theme_combo.addItems(themes)
        layout.addRow(QLabel("Select Theme:"), self.theme_combo)

        # Option to edit the selected theme
        edit_theme_button = QPushButton("Edit Theme")
        edit_theme_button.clicked.connect(self.edit_theme)
        layout.addRow(edit_theme_button)

        # Open the app in full screen mode or 1024x768, 1280x720, 1920x1080
        self.fullscreen_checkbox = QCheckBox("Open in Full Screen Mode")
        self.fullscreen_checkbox.setChecked(True)
        layout.addRow(self.fullscreen_checkbox)

        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["1024x768", "1280x720", "1920x1080"])
        layout.addRow(QLabel("Resolution:"), self.resolution_combo)

        # Font size slider
        font_size_slider = QSlider(Qt.Horizontal)
        font_size_slider.setMinimum(10)
        font_size_slider.setMaximum(30)
        font_size_slider.setValue(14)  # Default value
        font_size_slider.valueChanged.connect(self.update_font_size)
        layout.addRow(QLabel("Universal Font Size:"), font_size_slider)

        self.styles_tab.setLayout(layout)

    def setup_upload_settings(self):
        layout = QVBoxLayout()
        self.upload_site_combo = QComboBox()
        self.upload_site_combo.addItems(["Select Site", "YouTube", "Vimeo", "Custom..."])
        self.upload_site_combo.currentIndexChanged.connect(self.check_custom_upload_site)

        self.custom_site_input = QLineEdit()
        self.custom_site_input.setPlaceholderText("Custom Upload Site URL")
        self.custom_site_input.setVisible(False)

        layout.addWidget(QLabel("Upload Site:"))
        layout.addWidget(self.upload_site_combo)
        layout.addWidget(self.custom_site_input)

        self.upload_settings_tab.setLayout(layout)

    def setup_download_settings(self):
        layout = QFormLayout()

        # Default download folder selection
        download_folder_label = QLabel("Default Download Folder:")
        download_folder_path = QLineEdit()
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(lambda: self.select_download_folder(download_folder_path))

        folder_layout = QHBoxLayout()
        folder_layout.addWidget(download_folder_path)
        folder_layout.addWidget(browse_button)
        layout.addRow(download_folder_label, folder_layout)

        # Playlist download option
        self.playlist_checkbox = QCheckBox("Download Playlists (True/False)")
        self.playlist_checkbox.setChecked(True)
        layout.addRow(self.playlist_checkbox)

        # Download thumbnails option
        self.download_thumbnails_checkbox = QCheckBox("Download Thumbnails")
        self.download_thumbnails_checkbox.setChecked(True)
        layout.addRow(self.download_thumbnails_checkbox)

        self.download_settings_tab.setLayout(layout)

    def setup_proxy_settings(self):
        layout = QFormLayout()

        # Proxy type (HTTP, SOCKS5, etc.)
        proxy_type_label = QLabel("Proxy Type:")
        self.proxy_type_combo = QComboBox()
        self.proxy_type_combo.addItems(["None", "HTTP", "SOCKS5"])
        layout.addRow(proxy_type_label, self.proxy_type_combo)

        # Proxy IP
        self.proxy_ip_input = QLineEdit()
        self.proxy_ip_input.setPlaceholderText("Proxy IP Address")
        layout.addRow(QLabel("Proxy IP:"), self.proxy_ip_input)

        # Proxy Port
        self.proxy_port_input = QLineEdit()
        self.proxy_port_input.setPlaceholderText("Proxy Port")
        layout.addRow(QLabel("Proxy Port:"), self.proxy_port_input)

        self.proxy_settings_tab.setLayout(layout)

    def select_download_folder(self, download_folder_path):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder", "")
        if folder:
            download_folder_path.setText(folder)

    def edit_theme(self):
        selected_theme = self.theme_combo.currentText()
        theme_file = os.path.join(os.getcwd(), 'themes', f"{selected_theme}.py")
        if os.path.exists(theme_file):
            os.startfile(theme_file)  # Replace with an editor tab if available

    def check_custom_upload_site(self, index):
        if self.upload_site_combo.currentText() == "Custom...":
            self.custom_site_input.setVisible(True)
        else:
            self.custom_site_input.setVisible(False)

    def update_font_size(self, value):
        font_size = f"{value}px"
        self.parent().setStyleSheet(f"* {{ font-size: {font_size}; }}")

    def get_playlist_setting(self):
        return self.download_thumbnails_checkbox.isChecked()


    def get_playlist_setting(self):
        return self.playlist_checkbox.isChecked()


    def save_download_info(self, data):
        downloads_path = os.path.join(os.getcwd(), 'data', 'downloads.json')
        try:
            if os.path.exists(downloads_path):
                with open(downloads_path, 'r') as file:
                    existing_data = json.load(file)
            else:
                existing_data = []

            existing_data.append(data)
            with open(downloads_path, 'w') as file:
                json.dump(existing_data, file, indent=4)
        except Exception as e:
            print(f"Error saving download information: {e}")

    def download_completed(self, video_title, video_url, video_size, video_duration):
        download_data = {
            "title": video_title,
            "url": video_url,
            "size": video_size,
            "duration": video_duration,
            "status": "completed"
        }
        self.save_download_info(download_data)
