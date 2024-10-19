import os
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QMenu, QAction, QMessageBox, QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class DownloadLaterTab(QWidget):
    def __init__(self, download_manager):
        super().__init__()
        self.download_manager = download_manager
        self.layout = QVBoxLayout()
        self.download_later_list = QListWidget()
        self.load_download_later_list()

        self.download_later_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.download_later_list.customContextMenuRequested.connect(self.show_context_menu)

        self.layout.addWidget(self.download_later_list)
        self.setLayout(self.layout)

    def load_download_later_list(self):
        json_file_path = os.path.join('data', 'download_later.json')
        if not os.path.exists(json_file_path):
            return
        with open(json_file_path, 'r', encoding='utf-8') as f:
            urls = json.load(f)
        self.download_later_list.clear()
        for url in urls:
            item = QListWidgetItem(url)
            self.download_later_list.addItem(item)

    def add_url(self, url):
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
            self.load_download_later_list()

    def remove_url(self, url):
        json_file_path = os.path.join('data', 'download_later.json')
        if not os.path.exists(json_file_path):
            return
        with open(json_file_path, 'r', encoding='utf-8') as f:
            urls = json.load(f)
        if url in urls:
            urls.remove(url)
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(urls, f, indent=4)
            self.load_download_later_list()

    def show_context_menu(self, position):
        item = self.download_later_list.itemAt(position)
        if item:
            menu = QMenu()
            download_action = QAction(QIcon("icons/download.png"), "Download Now", self)
            remove_action = QAction(QIcon("icons/remove.png"), "Remove", self)

            download_action.triggered.connect(lambda: self.download_now(item))
            remove_action.triggered.connect(lambda: self.remove_item(item))

            menu.addAction(download_action)
            menu.addAction(remove_action)
            menu.exec_(self.download_later_list.viewport().mapToGlobal(position))

    def download_now(self, item):
        url = item.text()
        self.remove_url(url)
        self.download_manager.add_new_download_tab_with_url(url)

    def remove_item(self, item):
        url = item.text()
        self.remove_url(url)

    def get_pending_downloads(self):
        json_file_path = os.path.join('data', 'download_later.json')
        if not os.path.exists(json_file_path):
            return []
        with open(json_file_path, 'r', encoding='utf-8') as f:
            urls = json.load(f)
        return urls
