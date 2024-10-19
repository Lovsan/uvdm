import os
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QMenu, QAction, QMessageBox, QListWidgetItem
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QIcon
from app.upload_worker import UploadWorker

class UploadsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.uploads_list = QListWidget()
        self.load_uploads_history()

        self.uploads_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.uploads_list.customContextMenuRequested.connect(self.show_context_menu)

        self.layout.addWidget(self.uploads_list)
        self.setLayout(self.layout)

    def load_uploads_history(self):
        json_file_path = os.path.join('data', 'uploads.json')
        if not os.path.exists(json_file_path):
            return
        with open(json_file_path, 'r', encoding='utf-8') as f:
            uploads = json.load(f)
        self.uploads_list.clear()
        for upload in uploads:
            item_text = f"{upload['filename']} - {upload['site']} - {upload['status']}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, upload)
            self.uploads_list.addItem(item)

    def add_upload_entry(self, upload_info):
        json_file_path = os.path.join('data', 'uploads.json')
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                uploads = json.load(f)
        else:
            uploads = []
        uploads.append(upload_info)
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(uploads, f, indent=4)
        self.load_uploads_history()

    def show_context_menu(self, position):
        item = self.uploads_list.itemAt(position)
        if item:
            menu = QMenu()
            reupload_action = QAction(QIcon("icons/upload.png"), "Reupload", self)
            delete_action = QAction(QIcon("icons/delete.png"), "Delete Entry", self)

            reupload_action.triggered.connect(lambda: self.reupload(item))
            delete_action.triggered.connect(lambda: self.delete_entry(item))

            menu.addAction(reupload_action)
            menu.addAction(delete_action)
            menu.exec_(self.uploads_list.viewport().mapToGlobal(position))

    def reupload(self, item):
        upload_info = item.data(Qt.UserRole)
        video_path = upload_info['path']
        # Assuming you have a method to get the settings_tab
        upload_site = self.parent().settings_tab.get_upload_site()
        if not upload_site:
            QMessageBox.warning(self, "Upload Error", "No upload site configured in settings.")
            return

        upload_thread = QThread()
        upload_worker = UploadWorker(video_path, upload_site, self.parent().settings_tab)
        upload_worker.moveToThread(upload_thread)

        def on_upload_complete(new_upload_info):
            QMessageBox.information(self, "Upload Complete", f"Video reuploaded successfully to {new_upload_info['site']}.")
            self.add_upload_entry(new_upload_info)
            upload_thread.quit()

        def on_upload_failed(error_message):
            QMessageBox.critical(self, "Upload Failed", error_message)
            upload_thread.quit()

        upload_worker.upload_finished.connect(on_upload_complete)
        upload_worker.upload_failed.connect(on_upload_failed)
        upload_thread.started.connect(upload_worker.run)
        upload_thread.finished.connect(upload_thread.deleteLater)

        upload_thread.start()

    def delete_entry(self, item):
        upload_info = item.data(Qt.UserRole)
        json_file_path = os.path.join('data', 'uploads.json')
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                uploads = json.load(f)
            uploads = [u for u in uploads if u != upload_info]
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(uploads, f, indent=4)
            self.load_uploads_history()
