import os
import json
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QTreeWidget, QScrollArea, QGridLayout, QMenu, QAction, QInputDialog,
    QMessageBox, QListWidgetItem, QTreeWidgetItem, QCheckBox, QTextEdit
)
from PyQt5.QtCore import Qt, QEvent, QThread
from PyQt5.QtGui import QIcon, QPixmap, QFontMetrics
from app.clickable_label import ClickableLabel
from app.upload_worker import UploadWorker

class DownloadsHistoryTab(QWidget):
    def __init__(self, settings_tab):
        super().__init__()
        self.settings_tab = settings_tab
        self.layout = QVBoxLayout()

        # Create search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search downloads...")
        self.search_bar.textChanged.connect(self.update_downloads_display)

        # Create separate buttons for Grid View and List View
        self.grid_view_button = QPushButton("Grid View")
        self.grid_view_button.clicked.connect(self.switch_to_grid_view)
        self.list_view_button = QPushButton("List View")
        self.list_view_button.clicked.connect(self.switch_to_list_view)

        # Add labels for total videos and total size
        self.total_videos_label = QLabel("Total Videos: 0")
        self.total_size_label = QLabel("Total Size: 0 MB")

        # Layout for the buttons, search bar, and labels
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.grid_view_button)
        top_layout.addWidget(self.list_view_button)
        top_layout.addWidget(self.search_bar)
        top_layout.addWidget(self.total_videos_label)
        top_layout.addWidget(self.total_size_label)
        self.layout.addLayout(top_layout)

        # Initialize the history tree (list view)
        self.history_tree = QTreeWidget()
        self.history_tree.setHeaderLabels(['Name', 'Size', 'Duration', 'Source', 'Path'])
        self.history_tree.setSortingEnabled(True)
        self.history_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.history_tree.customContextMenuRequested.connect(self.show_context_menu)
        self.history_tree.itemDoubleClicked.connect(self.item_double_clicked)

        # Initialize the scroll area for grid view
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.grid_layout = QGridLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)

        # Initially, add the QTreeWidget (list view) to the layout
        self.layout.addWidget(self.history_tree)

        self.setLayout(self.layout)

        self.current_view = 'list'
        self.downloads_data = []

        self.load_downloads_history()
        self.load_default_view()

    def load_default_view(self):
        settings_path = os.path.join('data', 'settings.json')
        if os.path.exists(settings_path):
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            default_view = settings.get("default_history_view", "List View")
            if default_view == "Grid View":
                self.switch_to_grid_view()
            else:
                self.switch_to_list_view()
        else:
            self.switch_to_list_view()

    def load_downloads_history(self):
        """Load the downloads history by reading from data/downloads.json."""
        self.downloads_data = []
        json_file_path = os.path.join('data', 'downloads.json')
        if not os.path.exists(json_file_path):
            return
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                self.downloads_data = json.load(f)
        except Exception as e:
            logging.error(f"Error loading downloads history: {e}")
        self.update_downloads_display()

    def item_double_clicked(self, item, column):
        data = item.data(0, Qt.UserRole)
        if data and data.get('type') == 'file':
            video_path = data.get('path')
            if video_path and os.path.exists(video_path):
                os.startfile(video_path)  # This will open the video with the default player
            else:
                QMessageBox.warning(self, "File Error", "The video file could not be found.")

    def show_context_menu(self, position):
        item = self.history_tree.itemAt(position)
        if item:
            menu = QMenu()
            data = item.data(0, Qt.UserRole)
            if data['type'] == 'file':
                play_action = QAction(QIcon("icons/play.png"), "Play", self)
                rename_action = QAction(QIcon("icons/rename.png"), "Rename", self)
                delete_action = QAction(QIcon("icons/delete.png"), "Delete", self)
                upload_action = QAction(QIcon("icons/upload.png"), "Upload", self)
                details_action = QAction(QIcon("icons/info.png"), "Details", self)

                play_action.triggered.connect(lambda: self.play_video(item))
                rename_action.triggered.connect(lambda: self.rename_video(item))
                delete_action.triggered.connect(lambda: self.delete_video(item))
                upload_action.triggered.connect(lambda: self.upload_video(item))
                details_action.triggered.connect(lambda: self.show_video_details(data))

                menu.addAction(play_action)
                menu.addAction(rename_action)
                menu.addAction(delete_action)
                menu.addAction(upload_action)
                menu.addAction(details_action)

            menu.exec_(self.history_tree.viewport().mapToGlobal(position))

    def switch_to_grid_view(self):
        self.clear_history_layout()
        self.current_view = 'grid'

        # Re-add buttons and search bar to the layout
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.grid_view_button)
        top_layout.addWidget(self.list_view_button)
        top_layout.addWidget(self.search_bar)
        top_layout.addWidget(self.total_videos_label)
        top_layout.addWidget(self.total_size_label)
        self.layout.addLayout(top_layout)

        # Hide the QTreeWidget (list view) and show the scroll area (grid view)
        self.history_tree.setVisible(False)
        self.scroll_area.setVisible(True)

        # Re-add the scroll area (grid view) to the layout
        self.layout.addWidget(self.scroll_area)
        self.update_downloads_display()  # Refresh the display

        # Ensure the grid layout adjusts when the window is resized
        self.scroll_area.resizeEvent = self.on_resize

    def switch_to_list_view(self):
        self.clear_history_layout()
        self.current_view = 'list'

        # Re-add buttons and search bar to the layout
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.grid_view_button)
        top_layout.addWidget(self.list_view_button)
        top_layout.addWidget(self.search_bar)
        top_layout.addWidget(self.total_videos_label)
        top_layout.addWidget(self.total_size_label)
        self.layout.addLayout(top_layout)

        # Show the QTreeWidget (history_tree) and hide the scroll area (grid view)
        self.history_tree.setVisible(True)
        self.scroll_area.setVisible(False)

        # Re-add the QTreeWidget (history_tree) to the layout
        self.layout.addWidget(self.history_tree)
        self.update_downloads_display()  # Refresh the display

    def update_downloads_display(self):
        """Update the displayed downloads based on the current view and search text."""
        search_text = self.search_bar.text().lower()
        filtered_downloads = [
            video for video in self.downloads_data
            if search_text in video.get('title', '').lower()
        ]

        # Calculate total videos and total size
        total_videos = len(filtered_downloads)
        total_size_bytes = sum(
            video.get('size', 0) for video in filtered_downloads
            if isinstance(video.get('size', 0), (int, float))
        )
        total_size_mb = total_size_bytes / (1024 * 1024)

        # Update labels
        self.total_videos_label.setText(f"Total Videos: {total_videos}")
        self.total_size_label.setText(f"Total Size: {total_size_mb:.2f} MB")

        if self.current_view == 'list':
            self.history_tree.clear()  # Clear previous items
            for video in filtered_downloads:
                if not video.get('path', '').lower().endswith(('.mp4', '.avi', '.mkv', '.flv', '.mov')):
                    continue  # Skip non-video files
                video_item = QTreeWidgetItem(self.history_tree)
                video_item.setText(0, video.get('title', 'Unknown Title'))
                size_value = video.get('size')
                if size_value and isinstance(size_value, (int, float)):
                    size_mb = size_value / (1024 * 1024)
                    size_text = f"{size_mb:.2f} MB"
                else:
                    size_text = "Unknown"
                video_item.setText(1, size_text)

                # Add video length (duration) in a human-readable format
                duration_seconds = video.get('duration', 0)
                if isinstance(duration_seconds, (int, float)):
                    minutes, seconds = divmod(int(duration_seconds), 60)
                    duration_text = f"{minutes} min {seconds} sec"
                else:
                    duration_text = "Unknown"

                video_item.setText(2, duration_text)  # Adding the video length in column 2
                video_item.setText(3, video.get('source_site', 'Unknown Source'))
                video_item.setText(4, video.get('path', 'Unknown Path'))
                video_item.setData(0, Qt.UserRole, {'type': 'file', 'path': video.get('path', '')})
        elif self.current_view == 'grid':
            # Clear the grid layout
            for i in reversed(range(self.grid_layout.count())):
                widget_to_remove = self.grid_layout.itemAt(i).widget()
                if widget_to_remove is not None:
                    self.grid_layout.removeWidget(widget_to_remove)
                    widget_to_remove.setParent(None)

            thumb_width = 300
            available_width = self.width()
            num_columns = max(1, available_width // (thumb_width + self.grid_layout.horizontalSpacing()))
            row = 0
            col = 0

            for video in filtered_downloads:
                if not video.get('path', '').lower().endswith(('.mp4', '.avi', '.mkv', '.flv', '.mov')):
                    continue  # Skip non-video files

                # Create a ClickableLabel for the thumbnail
                thumbnail_label = ClickableLabel()
                thumbnail_path = video.get('thumbnail', '')
                if os.path.exists(thumbnail_path):
                    pixmap = QPixmap(thumbnail_path)
                    # Scale pixmap to desired width, keep aspect ratio
                    scaled_pixmap = pixmap.scaled(thumb_width, thumb_width, Qt.KeepAspectRatio)
                    thumbnail_label.setPixmap(scaled_pixmap)
                else:
                    thumbnail_label.setText("No Thumbnail")
                    thumbnail_label.setFixedWidth(thumb_width)
                    thumbnail_label.setFixedHeight(thumb_width)

                # Store video data in the label
                thumbnail_label.setProperty('video_data', video)
                thumbnail_label.clicked.connect(self.grid_item_clicked)

                # Create a QLabel for the title
                title_label = QLabel(video.get('title', 'Unknown Title'))
                # Limit the width of the title label
                title_label.setFixedWidth(thumb_width)
                # Set word wrap and elide
                title_label.setWordWrap(False)
                title_label.setAlignment(Qt.AlignCenter)
                title_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
                metrics = title_label.fontMetrics()
                elided_text = metrics.elidedText(title_label.text(), Qt.ElideRight, thumb_width)
                title_label.setText(elided_text)
                title_label.setToolTip(video.get('title', 'Unknown Title'))

                # Add the thumbnail and title to the grid layout
                self.grid_layout.addWidget(thumbnail_label, row, col, alignment=Qt.AlignCenter)
                self.grid_layout.addWidget(title_label, row + 1, col, alignment=Qt.AlignCenter)

                col += 1
                if col >= num_columns:
                    col = 0
                    row += 2

            self.scroll_widget.adjustSize()
            self.scroll_area.adjustSize()

    def clear_history_layout(self):
        # Only remove widgets from the layout, don't delete them
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)  # Detach the widget, but don't delete

    def grid_item_clicked(self):
        label = self.sender()
        video_data = label.property('video_data')
        if video_data:
            # Simulate right-click menu
            menu = QMenu()
            play_action = QAction(QIcon("icons/play.png"), "Play", self)
            rename_action = QAction(QIcon("icons/rename.png"), "Rename", self)
            delete_action = QAction(QIcon("icons/delete.png"), "Delete", self)
            upload_action = QAction(QIcon("icons/upload.png"), "Upload", self)
            details_action = QAction(QIcon("icons/info.png"), "Details", self)

            play_action.triggered.connect(lambda: self.play_video_grid(video_data))
            rename_action.triggered.connect(lambda: self.rename_video_grid(video_data))
            delete_action.triggered.connect(lambda: self.delete_video_grid(video_data))
            upload_action.triggered.connect(lambda: self.upload_video_grid(video_data))
            details_action.triggered.connect(lambda: self.show_video_details(video_data))

            menu.addAction(play_action)
            menu.addAction(rename_action)
            menu.addAction(delete_action)
            menu.addAction(upload_action)
            menu.addAction(details_action)

            cursor_pos = self.cursor().pos()
            menu.exec_(cursor_pos)

    # Methods for playing, renaming, deleting, uploading videos in grid and list views

    def play_video(self, item):
        data = item.data(0, Qt.UserRole)
        video_path = data.get('path')
        if video_path and os.path.exists(video_path):
            os.startfile(video_path)
        else:
            QMessageBox.warning(self, "File Error", "The video file could not be found.")

    def rename_video(self, item):
        data = item.data(0, Qt.UserRole)
        old_path = data.get('path')
        if old_path and os.path.exists(old_path):
            new_name, ok = QInputDialog.getText(self, "Rename Video", "Enter new name:")
            if ok and new_name:
                new_name = new_name.strip()
                new_path = os.path.join(os.path.dirname(old_path), new_name + os.path.splitext(old_path)[1])
                os.rename(old_path, new_path)
                data['path'] = new_path
                data['title'] = new_name
                self.save_downloads_data()
                self.load_downloads_history()
        else:
            QMessageBox.warning(self, "File Error", "The video file could not be found.")

    def delete_video(self, item):
        data = item.data(0, Qt.UserRole)
        video_path = data.get('path')
        if video_path and os.path.exists(video_path):
            confirm = QMessageBox.question(self, "Delete Video", "Are you sure you want to delete this video?")
            if confirm == QMessageBox.Yes:
                os.remove(video_path)
                self.downloads_data.remove(data)
                self.save_downloads_data()
                self.load_downloads_history()
        else:
            QMessageBox.warning(self, "File Error", "The video file could not be found.")

    def upload_video(self, item):
        data = item.data(0, Qt.UserRole)
        video_path = data.get('path')
        if video_path and os.path.exists(video_path):
            upload_site = self.settings_tab.get_upload_site()
            if not upload_site:
                QMessageBox.warning(self, "Upload Error", "No upload site configured in settings.")
                return

            self.upload_thread = QThread()
            self.upload_worker = UploadWorker(video_path, upload_site, self.settings_tab)
            self.upload_worker.moveToThread(self.upload_thread)

            def on_upload_complete(upload_info):
                QMessageBox.information(self, "Upload Complete", f"Video uploaded successfully to {upload_info['site']}.")
                self.upload_thread.quit()

            def on_upload_failed(error_message):
                QMessageBox.critical(self, "Upload Failed", error_message)
                self.upload_thread.quit()

            self.upload_worker.upload_finished.connect(on_upload_complete)
            self.upload_worker.upload_failed.connect(on_upload_failed)
            self.upload_thread.started.connect(self.upload_worker.run)
            self.upload_thread.finished.connect(self.upload_thread.deleteLater)

            self.upload_thread.start()
        else:
            QMessageBox.warning(self, "File Error", "The video file could not be found.")

    def show_video_details(self, video_data):
        # Format size
        size_value = video_data.get('size')
        if size_value and isinstance(size_value, (int, float)):
            size_mb = size_value / (1024 * 1024)
            size_text = f"{size_mb:.2f} MB"
        else:
            size_text = "Unknown"

        # Format duration
        duration_seconds = video_data.get('duration', 0)
        if isinstance(duration_seconds, (int, float)):
            minutes, seconds = divmod(int(duration_seconds), 60)
            duration_text = f"{minutes} min {seconds} sec"
        else:
            duration_text = "Unknown"

        details = (
            f"Title: {video_data.get('title', 'Unknown Title')}\n"
            f"Size: {size_text}\n"
            f"Duration: {duration_text}\n"
            f"Source: {video_data.get('source_site', 'Unknown Source')}\n"
            f"Path: {video_data.get('path', 'Unknown Path')}\n"
        )
        QMessageBox.information(self, "Video Details", details)

    def save_downloads_data(self):
        json_file_path = os.path.join('data', 'downloads.json')
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.downloads_data, f, indent=4)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_grid_columns()

    def on_resize(self, event):
        self.adjust_grid_columns()

    def adjust_grid_columns(self):
        if self.current_view != 'grid':
            return

        thumb_width = 300
        available_width = self.scroll_area.viewport().width()
        num_columns = max(1, available_width // (thumb_width + self.grid_layout.horizontalSpacing()))
        if num_columns <= 0:
            num_columns = 1

        # Re-arrange the items in the grid layout
        count = self.grid_layout.count()
        row = 0
        col = 0
        for index in range(0, count, 2):  # Each item is two widgets: thumbnail and title
            thumbnail_item = self.grid_layout.itemAt(index)
            title_item = self.grid_layout.itemAt(index + 1)
            self.grid_layout.addItem(thumbnail_item, row, col)
            self.grid_layout.addItem(title_item, row + 1, col)
            col += 1
            if col >= num_columns:
                col = 0
                row += 2

        self.scroll_widget.adjustSize()
