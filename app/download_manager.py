# app/downloads_manager.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QPushButton
from app.download_tab import YTDLPTab
from app.download_history_tab import DownloadsHistoryTab
from app.download_later_tab import DownloadLaterTab
from app.uploads_tab import UploadsTab

class DownloadsManager(QWidget):
    def __init__(self, settings_tab, main_window):
        super().__init__()
        self.settings_tab = settings_tab
        self.main_window = main_window
        self.layout = QVBoxLayout()
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)  # Enable the close button on tabs
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.download_queue = []
        self.active_workers = []

        self.add_download_tab_button = QPushButton("New Download Tab")
        self.add_download_tab_button.clicked.connect(self.add_new_download_tab)

        self.layout.addWidget(self.tab_widget)
        self.layout.addWidget(self.add_download_tab_button)
        self.setLayout(self.layout)

        self.history_tab = DownloadsHistoryTab(self.settings_tab)  # Pass settings_tab
        self.download_later_tab = DownloadLaterTab(self)  # Initialize Download Later tab
        self.uploads_tab = UploadsTab()  # Initialize Uploads tab

        # Add the first download tab
        self.add_new_download_tab()

    def add_to_download_queue(self, url):
        self.download_queue.append(url)
        self.update_download_queue_label()

    def update_download_queue_label(self):
        num_queue = len(self.download_queue)
        # Include downloads from active playlist workers
        for tab_index in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(tab_index)
            if hasattr(tab, 'worker') and hasattr(tab.worker, 'total_videos'):
                num_queue += tab.worker.total_videos - tab.worker.videos_downloaded
        # Include downloads from download_later.json
        num_queue += len(self.download_later_tab.get_pending_downloads())
        self.main_window.download_queue_label.setText(f"Downloads in Queue: {num_queue}")

    def add_new_download_tab(self):
        """Add a new download tab to allow concurrent downloads."""
        tab_index = self.tab_widget.count()  # Get the current tab index
        new_tab = YTDLPTab(self.settings_tab, self, self.history_tab, tab_index, self.tab_widget, self.download_later_tab)
        self.tab_widget.addTab(new_tab, f"Download {tab_index + 1}")
        self.tab_widget.setCurrentWidget(new_tab)

    def add_new_download_tab_with_url(self, url):
        """Add a new download tab with the specified URL."""
        self.add_new_download_tab()
        # Get the newly added tab
        new_tab = self.tab_widget.currentWidget()
        new_tab.url_input.setText(url)
        # Optionally, start the download immediately
        new_tab.start_download_thread()

    def close_tab(self, index):
        """Handle tab close action."""
        self.tab_widget.removeTab(index)
