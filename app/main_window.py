import os
import sys
import psutil
import json
from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QStatusBar, QLabel, QApplication, QMessageBox, QAction, QMenu
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
from app.settings_tab import SettingsTab
from app.download_manager import DownloadsManager
from app.logs_tab import LogsTab
from app.editor import EditorTab
from app.batch_downloader import BatchDownloader
from app.about_tab import AboutTab
from app.clipboard_monitor import ClipboardMonitor
from app.themes import themes
from app.my_playlists_tab import MyPlaylistsTab
from app.license_dialog import show_license_dialog
#from app.my_playlists import PlaylistManager


class YTDLPApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ultimate Video Download Manager - Lovsan's Toolbox")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("icons/app.png"))

        self.tabs = QTabWidget()
        self.settings_tab = SettingsTab()
        self.download_manager = DownloadsManager(self.settings_tab, self)  # Pass settings tab
        self.logs_tab = LogsTab()  # For download and error logs
        self.history_tab = self.download_manager.history_tab  # Downloads history tab
        self.download_later_tab = self.download_manager.download_later_tab  # Download Later tab
        self.uploads_tab = self.download_manager.uploads_tab  # Uploads tab
        self.batch_downloader_tab = BatchDownloader(self.settings_tab)  # Batch Downloader tab
        self.editor_tab = EditorTab()  # Editor tab
        self.playlists_tab = MyPlaylistsTab() #  My Playlists tab

        # Add the tabs to the main window
        self.tabs.addTab(self.download_manager, "Downloads")
        self.tabs.addTab(self.batch_downloader_tab, "Batch Downloader")
        self.tabs.addTab(self.history_tab, "Download History")
        self.tabs.addTab(self.download_later_tab, "Download Later")
        self.tabs.addTab(self.playlists_tab, "My Playlists")
        self.tabs.addTab(self.uploads_tab, "Uploads")
        self.tabs.addTab(self.settings_tab, "Settings")
        self.tabs.addTab(self.logs_tab, "Logs")
        self.tabs.addTab(self.editor_tab, "Editor")
        self.tabs.addTab(AboutTab(), "About")

        self.setCentralWidget(self.tabs)

        # Create menu bar
        self.create_menu_bar()

        # Apply default theme
        self.apply_theme_on_startup()

        # Initialize and start the clipboard monitor
        self.clipboard_monitor = ClipboardMonitor()
        self.clipboard_monitor.new_url_found.connect(self.handle_new_clipboard_url)
        self.clipboard_monitor.start()

        # Add system statistics
        self.init_system_statistics()
        
        # Optional: Check license on startup (non-blocking)
        self.check_license_on_startup()

    def check_license_on_startup(self):
        """Check license on startup (non-blocking and non-intrusive)."""
        try:
            from app.license_client import LicenseClient
            
            # Get server URL from environment or config
            server_url = os.environ.get('UVDM_LICENSE_SERVER')
            
            # Only check if server URL is configured
            if server_url:
                client = LicenseClient(server_url=server_url)
                cache = client._load_cache()
                
                if cache.get('license_key'):
                    # Verify cached license (with offline fallback)
                    result = client.verify_license(cache['license_key'], offline_mode=False)
                    
                    if not result.get('valid'):
                        # Show non-intrusive status bar message
                        self.statusBar.showMessage(
                            "License verification failed. Check Help > License Manager for details.",
                            10000  # Show for 10 seconds
                        )
                else:
                    # No license found - show friendly message
                    self.statusBar.showMessage(
                        "No license found. Visit Help > License Manager to activate your license.",
                        10000
                    )
        except Exception as e:
            # Silent fail - don't block the application
            print(f"License check error (non-critical): {e}")

    def create_menu_bar(self):
        """Create the application menu bar."""
        menubar = self.menuBar()
        
        # Help menu
        help_menu = menubar.addMenu('&Help')
        
        # License manager action
        license_action = QAction('&License Manager', self)
        license_action.setStatusTip('Manage your UVDM license')
        license_action.triggered.connect(self.show_license_manager)
        help_menu.addAction(license_action)
        
        # About action
        about_action = QAction('&About', self)
        about_action.setStatusTip('About UVDM')
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def show_license_manager(self):
        """Show the license manager dialog."""
        server_url = os.environ.get('UVDM_LICENSE_SERVER', 'http://localhost:5000')
        show_license_dialog(self, server_url)
    
    def show_about(self):
        """Show about information."""
        # Switch to About tab
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == "About":
                self.tabs.setCurrentIndex(i)
                break

    def init_system_statistics(self):
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.cpu_label = QLabel("CPU: 0%")
        self.ram_label = QLabel("RAM: 0%")
        self.disk_label = QLabel("Disk: 0%")
        self.threads_label = QLabel("Threads: 0")
        self.download_queue_label = QLabel("Downloads in Queue: 0")
        self.statusBar.addPermanentWidget(self.cpu_label)
        self.statusBar.addPermanentWidget(self.ram_label)
        self.statusBar.addPermanentWidget(self.disk_label)
        self.statusBar.addPermanentWidget(self.threads_label)
        self.statusBar.addPermanentWidget(self.download_queue_label)

        self.storage_label = QLabel("Storage: 0 GB / 0 GB")
        self.network_label = QLabel("Network Usage: 0 KB/s")
        self.active_downloads_label = QLabel("Active Downloads: 0")
        self.statusBar.addPermanentWidget(self.storage_label)
        self.statusBar.addPermanentWidget(self.network_label)
        self.statusBar.addPermanentWidget(self.active_downloads_label)

        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_system_statistics)
        self.stats_timer.start(2000)  # Update every 2 seconds

    def update_system_statistics(self):
        process = psutil.Process(os.getpid())
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        threads = process.num_threads()
        self.cpu_label.setText(f"CPU: {cpu_usage}%")
        self.ram_label.setText(f"RAM: {ram_usage}%")
        self.disk_label.setText(f"Disk: {disk_usage}%")
        self.threads_label.setText(f"Threads: {threads}")

        # Update storage usage
        storage = psutil.disk_usage('/')
        total_gb = storage.total / (1024 ** 3)
        used_gb = storage.used / (1024 ** 3)
        self.storage_label.setText(f"Storage: {used_gb:.2f} GB / {total_gb:.2f} GB")

        # Update network usage
        net_io = psutil.net_io_counters()
        sent_bytes = net_io.bytes_sent / 1024  # Convert to KB
        recv_bytes = net_io.bytes_recv / 1024  # Convert to KB
        self.network_label.setText(f"Network Usage: {sent_bytes:.2f} KB sent, {recv_bytes:.2f} KB received")

        # Update active downloads
        active_downloads = self.get_active_download_count()
        self.active_downloads_label.setText(f"Active Downloads: {active_downloads}")

    def get_active_download_count(self):
        """Returns the number of active downloads."""
        return len(self.download_manager.download_queue)

    def handle_new_clipboard_url(self, url):
        """Handle new URL found in the clipboard."""
        # Show a message box to ask the user
        reply = QMessageBox.question(self, 'Download Video?', f'Do you want to download this video?\n{url}', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            # Add a new download tab with the URL
            self.download_manager.add_new_download_tab_with_url(url)
        elif reply == QMessageBox.No:
            # Save to Download Later list
            self.download_later_tab.add_url(url)
            QMessageBox.information(self, "Saved for Later", "The video URL has been saved for later download.")

    def apply_theme_on_startup(self):
        settings_path = os.path.join('data', "settings.json")
        if os.path.exists(settings_path):
            with open(settings_path, "r", encoding='utf-8') as f:
                settings = json.load(f)
                theme = settings.get("theme", "Grey, White, Black")
                self.apply_theme(theme)
        else:
            # Apply default theme
            self.apply_theme("Grey, White, Black")

    def apply_theme(self, theme_name):
        theme = themes.get(theme_name, themes["Grey, White, Black"])
        stylesheet = f"""
            QMainWindow {{
                background-color: {theme['background-color']};
            }}
            QWidget {{
                background-color: {theme['background-color']};
                color: {theme['text-color']};
            }}
            QLabel, QPushButton, QComboBox, QLineEdit, QTreeWidget, QListWidget, QProgressBar {{
                color: {theme['text-color']};
                background-color: {theme['button-background']};
            }}
            QPushButton:hover {{
                background-color: {theme['button-hover']};
            }}
            QProgressBar::chunk {{
                background-color: {theme['progress-bar']};
            }}
            QScrollBar {{
                background-color: {theme['button-background']};
            }}
            QMenu {{
                background-color: {theme['button-background']};
                color: {theme['text-color']};
            }}
            QMenu::item:selected {{
                background-color: {theme['button-hover']};
            }}
        """
        self.setStyleSheet(stylesheet)
