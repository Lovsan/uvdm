def apply_theme(self, theme_name):
        #self.parent().apply_theme(theme_name)
        self.window().apply_theme(theme_name)


    #def apply_theme(self, theme_name):
        theme = themes.get(theme_name, themes["Grey, White, Black"])
        stylesheet = f"""
            QMainWindow {{
                background-color: {theme['background-color']};
            }}
            QLabel, QPushButton, QComboBox {{
                color: {theme['text-color']};
                background-color: {theme['button-background']};
            }}
            QPushButton:hover {{
                background-color: {theme['button-hover']};
            }}
            QProgressBar {{
                background-color: {theme['button-background']};
                border: 1px solid {theme['button-hover']};
            }}
            QProgressBar::chunk {{
                background-color: {theme['progress-bar']};
            }}
        """
        self.parent().setStyleSheet(stylesheet)

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

# Add this class definition
class ClickableLabel(QLabel):
    clicked = pyqtSignal(QMouseEvent)

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        self.clicked.emit(event)

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
        self.history_tree.setSortingEnabled(True)  # Enable sorting by columns
        self.history_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.history_tree.customContextMenuRequested.connect(self.show_context_menu)
        self.history_tree.itemDoubleClicked.connect(self.item_double_clicked)

        # Initialize the scroll area for grid view
        self.scroll_area = QScrollArea()  # Ensure scroll_area is initialized here
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.grid_layout = QGridLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)

        # Initially, add the QTreeWidget (list view) to the layout
        self.layout.addWidget(self.history_tree)

        self.setLayout(self.layout)

        self.current_view = 'list'  # Keep track of the current view
        self.downloads_data = []    # Store downloads data

        self.load_downloads_history()

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

            # Load the default view
        self.load_default_view()

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

    def show_context_menu(self, position):
        item = self.history_tree.itemAt(position)
        if item:
            menu = QMenu()
            data = item.data(0, Qt.UserRole)
            if data['type'] == 'file':
                play_action = QAction(QIcon("icons/play.png"), "Play", self)
                rename_action = QAction(QIcon("icons/rename.png"),"Rename", self)
                delete_action = QAction(QIcon("icons/delete.png"),"Delete", self)
                upload_action = QAction(QIcon("icons/uploadplay.png"),"Upload", self)
                details_action = QAction(QIcon("icons/info.png"),"Details", self)

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
        self.scroll_area.setVisible(False)  # If using scroll_area for grid view

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

    def grid_item_clicked(self, event):
        label = self.sender()
        video_data = label.property('video_data')
        if video_data:
            # Simulate right-click menu
            menu = QMenu()
            play_action = QAction(QIcon("icons/play.png"),"Play", self)
            rename_action = QAction(QIcon("icons/rename.png"),"Rename", self)
            delete_action = QAction(QIcon("icons/delete.png"),"Delete", self)
            upload_action = QAction(QIcon("icons/upload.png"),"Upload", self)
            details_action = QAction(QIcon("icons/info.png"),"Details", self)

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

            menu.exec_(event.globalPos())

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


    def play_video_grid(self, video_data):
        video_path = video_data["path"]
        if os.path.exists(video_path):
            os.startfile(video_path)
        else:
            QMessageBox.warning(self, "File Not Found", "The video file could not be found.")

    def rename_video_grid(self, video_data):
        old_path = video_data["path"]
        new_name, ok = QInputDialog.getText(self, "Rename Video", "Enter new name:", text=os.path.basename(old_path))
        if ok and new_name:
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            if not new_name.endswith(os.path.splitext(old_path)[1]):
                new_path += os.path.splitext(old_path)[1]
            try:
                os.rename(old_path, new_path)
                video_data["path"] = new_path
                # Now update the downloads.json file
                self.update_downloads_json(old_path, new_path)
                self.switch_to_grid_view()  # Refresh the grid view
            except Exception as e:
                QMessageBox.critical(self, "Rename Error", f"An error occurred while renaming: {str(e)}")

    def delete_video_grid(self, video_data):
        video_path = video_data["path"]
        confirm = QMessageBox.question(self, "Delete Video", f"Are you sure you want to delete {os.path.basename(video_path)}?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                if os.path.exists(video_path):
                    os.remove(video_path)
                # Remove from downloads.json
                self.remove_from_downloads_json(video_path)
                self.switch_to_grid_view()  # Refresh the grid view
            except Exception as e:
                QMessageBox.critical(self, "Delete Error", f"An error occurred while deleting the video: {str(e)}")

    def upload_video_grid(self, video_data):
        video_path = video_data["path"]
        upload_site = self.settings_tab.get_upload_site()
        if not upload_site:
            QMessageBox.warning(self, "Upload Error", "No upload site configured in settings.")
            return

        upload_thread = QThread()
        upload_worker = UploadWorker(video_path, upload_site, self.settings_tab)
        upload_worker.moveToThread(upload_thread)

        def on_upload_complete(upload_info):
            QMessageBox.information(self, "Upload Complete", f"Video uploaded successfully to {upload_info['site']}.")
            upload_thread.quit()

        def on_upload_failed(error_message):
            QMessageBox.critical(self, "Upload Failed", error_message)
            upload_thread.quit()

        upload_worker.upload_finished.connect(on_upload_complete)
        upload_worker.upload_failed.connect(on_upload_failed)
        upload_thread.started.connect(upload_worker.run)
        upload_thread.finished.connect(upload_thread.deleteLater)

        upload_thread.start()

    def play_video(self, item):
        data = item.data(0, Qt.UserRole)
        video_path = data["path"]
        if os.path.exists(video_path):
            os.startfile(video_path)
        else:
            QMessageBox.warning(self, "File Not Found", "The video file could not be found.")

    def rename_video(self, item):
        data = item.data(0, Qt.UserRole)
        old_path = data["path"]
        new_name, ok = QInputDialog.getText(self, "Rename Video", "Enter new name:", text=os.path.basename(old_path))
        if ok and new_name:
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            if not new_name.endswith(os.path.splitext(old_path)[1]):
                new_path += os.path.splitext(old_path)[1]
            try:
                os.rename(old_path, new_path)
                data["path"] = new_path
                item.setText(0, os.path.basename(new_path))
                # Now update the downloads.json file
                self.update_downloads_json(old_path, new_path)
            except Exception as e:
                QMessageBox.critical(self, "Rename Error", f"An error occurred while renaming: {str(e)}")

    def update_downloads_json(self, old_path, new_path):
        json_file_path = os.path.join('data', 'downloads.json')
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                downloads = json.load(f)

            # Update the path in the json
            for entry in downloads:
                if entry["path"] == old_path:
                    entry["path"] = new_path
                    break

            # Write the updated json back to file
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(downloads, f, indent=4, ensure_ascii=False)

    def remove_from_downloads_json(self, video_path):
        json_file_path = os.path.join('data', 'downloads.json')
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                downloads = json.load(f)

            downloads = [entry for entry in downloads if entry["path"] != video_path]

            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(downloads, f, indent=4, ensure_ascii=False)

    def delete_video(self, item):
        data = item.data(0, Qt.UserRole)
        video_path = data["path"]
        confirm = QMessageBox.question(self, "Delete Video", f"Are you sure you want to delete {os.path.basename(video_path)}?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                if os.path.exists(video_path):
                    os.remove(video_path)
                    index = self.history_tree.indexOfTopLevelItem(item)
                    self.history_tree.takeTopLevelItem(index)
                # Remove from downloads.json
                self.remove_from_downloads_json(video_path)
            except Exception as e:
                QMessageBox.critical(self, "Delete Error", f"An error occurred while deleting the video: {str(e)}")

    def upload_video(self, item):
        data = item.data(0, Qt.UserRole)
        video_path = data["path"]
        upload_site = self.settings_tab.get_upload_site()
        if not upload_site:
            QMessageBox.warning(self, "Upload Error", "No upload site configured in settings.")
            return

        upload_thread = QThread()
        upload_worker = UploadWorker(video_path, upload_site, self.settings_tab)
        upload_worker.moveToThread(upload_thread)

        def on_upload_complete(upload_info):
            QMessageBox.information(self, "Upload Complete", f"Video uploaded successfully to {upload_info['site']}.")
            upload_thread.quit()

        def on_upload_failed(error_message):
            QMessageBox.critical(self, "Upload Failed", error_message)
            upload_thread.quit()

        upload_worker.upload_finished.connect(on_upload_complete)
        upload_worker.upload_failed.connect(on_upload_failed)
        upload_thread.started.connect(upload_worker.run)
        upload_thread.finished.connect(upload_thread.deleteLater)

        upload_thread.start()

    def item_double_clicked(self, item, column):
        data = item.data(0, Qt.UserRole)
        if data.get('type') == 'file':
            self.play_video(item)

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
            download_action = QAction(QIcon("icons/download.png"),"Download Now", self)
            remove_action = QAction(QIcon("icons/remove.png"),"Remove", self)

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
            reupload_action = QAction(QIcon("icons/upload.png"),"Reupload", self)
            delete_action = QAction(QIcon("icons/delete.png"),"Delete Entry", self)

            reupload_action.triggered.connect(lambda: self.reupload(item))
            delete_action.triggered.connect(lambda: self.delete_entry(item))

            menu.addAction(reupload_action)
            menu.addAction(delete_action)
            menu.exec_(self.uploads_list.viewport().mapToGlobal(position))

    def reupload(self, item):
        upload_info = item.data(Qt.UserRole)
        video_path = upload_info['path']
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


class IntroThread(QThread):
    update_text = pyqtSignal(str)
    clear_text = pyqtSignal()

    def __init__(self, ascii_art, about_info):
        super().__init__()
        self.ascii_art = ascii_art
        self.about_info = about_info

    def run(self):
        # Typewriter effect for ASCII art
        for char in self.ascii_art:
            self.update_text.emit(char)
            time.sleep(0.02)
        time.sleep(0.5)
        # Blink effect for ASCII art
        for _ in range(1):
            self.clear_text.emit()
            time.sleep(0.3)
            self.update_text.emit(self.ascii_art)
            time.sleep(0.3)
        # Typewriter effect for about info
        self.clear_text.emit()
        for char in self.about_info:
            self.update_text.emit(char)
            time.sleep(0.01)


class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        # ASCII art intro and about info
        self.ascii_art = r"""
  _    _  __     __ ____  __  __     
 | |  | | \ \   / /|  _ \|  \/  |    
 | |  | |  \ \ / / | | | | |\/| |    
 | |__| |   \ V /  | |_| | |  | |    
  \____/     \_/   |____/|_|  |_|    
                                    
  Ultimate Video Download Manager
"""
        self.about_info = r"""
  _    _  __     __ ____  __  __     
 | |  | | \ \   / /|  _ \|  \/  |    
 | |  | |  \ \ / / | | | | |\/| |    
 | |__| |   \ V /  | |_| | |  | |    
  \____/     \_/   |____/|_|  |_|    
                                    
                                     
  Ultimate Video Download Manager
  
Ultimate Video Download Manager (UVDM) is your one-stop solution for downloading and managing videos effortlessly.

Features:
- Download videos from popular websites with ease.
- Monitors clipboard for supported video links and prompts for download.
- Supports multiple video formats: MP3, MP4, AVI, and more.
- Single file downloads, playlist downloads, and batch downloads.
- Integrated download history with list view or grid view (with thumbnails), showing names, lengths, and sizes.
- Search downloaded files and play them in your default system player.
- Sorting and filtering options for downloaded content.
- Customizable themes for a personalized experience.
- Manage downloaded files directly within the app.
- Resume, rename, or delete downloads with a simple click.
- Choose video quality and format before downloading.
- Multi-threaded downloads for faster performance.
- View and manage active downloads.

Powered by yt-dlp, a powerful command-line tool for downloading videos from popular websites.

GitHub Repository:
- Ultimate Video Download Manager: https://github.com/username/uvdm
- yt-dlp: https://github.com/yt-dlp/yt-dlp

Enjoy a seamless video downloading experience!
"""

        # Label to display the intro text
        self.intro_label = QLabel()
        self.intro_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.intro_label)

        # Run typewriter effect in a separate QThread to avoid freezing UI
        self.intro_thread = IntroThread(self.ascii_art, self.about_info)
        self.intro_thread.update_text.connect(self.update_intro_text)
        self.intro_thread.clear_text.connect(self.clear_intro_text)
        self.intro_thread.start()

        # Add a button to view supported sites
        self.supported_sites_button = QPushButton("View Supported Sites")
        self.supported_sites_button.clicked.connect(self.open_supported_sites)
        self.layout.addWidget(self.supported_sites_button, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)

    def update_intro_text(self, char):
        current_text = self.intro_label.text() + char
        self.intro_label.setText(current_text)

    def clear_intro_text(self):
        self.intro_label.setText("")

    def open_supported_sites(self):
        # Create a new window to display supported sites
        self.supported_sites_window = QWidget()
        self.supported_sites_window.setWindowTitle("Supported Sites")
        layout = QVBoxLayout()

        # Correctly call list_extractors without arguments
        ie_list = yt_dlp.extractor.list_extractors()

        # Retrieve list of supported sites
        sites = sorted(set(ie.IE_NAME for ie in ie_list if ie.IE_NAME != 'generic'))

        # Create a QTextEdit to display the sites
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setText("\n".join(sites))
        layout.addWidget(text_edit)

        self.supported_sites_window.setLayout(layout)
        self.supported_sites_window.resize(400, 600)
        self.supported_sites_window.show()

class EditorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.open_button = QPushButton("Open File")
        self.open_button.clicked.connect(self.open_file)

        self.save_button = QPushButton("Save File")
        self.save_button.clicked.connect(self.save_file)
        self.save_button.setEnabled(False)  # Disable until a file is opened

        self.text_edit = QTextEdit()

        self.layout.addWidget(self.open_button)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.text_edit)
        self.setLayout(self.layout)

        self.current_file_path = None

    def open_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)", options=options)
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_edit.setText(content)
                self.current_file_path = file_path
                self.save_button.setEnabled(True)
            except Exception as e:
                QMessageBox.critical(self, "Open File", f"Failed to open file: {e}")

    def save_file(self):
        if self.current_file_path:
            try:
                with open(self.current_file_path, 'w', encoding='utf-8') as f:
                    content = self.text_edit.toPlainText()
                    f.write(content)
                QMessageBox.information(self, "Save File", f"File saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Save File", f"Failed to save file: {e}")


class LogsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # Add Download Logs section
        self.download_logs_label = QLabel("Download Logs")
        self.download_logs_output = QTextEdit()
        self.download_logs_output.setReadOnly(False)
        self.load_logs(self.download_logs_output, 'logs.log')

        # Add Save button for download logs
        self.save_download_logs_button = QPushButton("Save Download Logs")
        self.save_download_logs_button.clicked.connect(lambda: self.save_logs(self.download_logs_output, 'logs.log'))

        # Add Error Logs section
        self.error_logs_label = QLabel("Error Logs")
        self.error_logs_output = QTextEdit()
        self.error_logs_output.setReadOnly(False)
        self.load_logs(self.error_logs_output, 'error_logs.log')

        # Add Save button for error logs
        self.save_error_logs_button = QPushButton("Save Error Logs")
        self.save_error_logs_button.clicked.connect(lambda: self.save_logs(self.error_logs_output, 'error_logs.log'))

        # Layout for logs
        self.layout.addWidget(self.download_logs_label)
        self.layout.addWidget(self.download_logs_output)
        self.layout.addWidget(self.save_download_logs_button)
        self.layout.addWidget(self.error_logs_label)
        self.layout.addWidget(self.error_logs_output)
        self.layout.addWidget(self.save_error_logs_button)

        self.setLayout(self.layout)

    def load_logs(self, text_widget, log_file):
        """Load log data from the given log file into the text widget."""
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r') as file:
                    logs = file.read()
                    text_widget.setText(logs)
            else:
                text_widget.setText(f"No logs found in {log_file}.")
                logging.warning(f"Log file {log_file} does not exist.")
        except Exception as e:
            logging.error(f"Failed to load log file {log_file}: {e}")
            text_widget.setText(f"Error loading log file {log_file}.")

    def save_logs(self, text_widget, log_file):
        """Save the contents of the text widget to the given log file."""
        try:
            with open(log_file, 'w') as file:
                logs = text_widget.toPlainText()
                file.write(logs)
            QMessageBox.information(self, "Save Logs", f"Logs saved to {log_file}.")
        except Exception as e:
            logging.error(f"Failed to save log file {log_file}: {e}")
            QMessageBox.critical(self, "Save Logs", f"Error saving log file {log_file}.")

class PlaylistLoader(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # Label to show playlist URL input
        self.url_label = QLabel("Enter Playlist URL:")
        self.layout.addWidget(self.url_label)

        # Button to load playlist
        self.load_button = QPushButton("Load Playlist")
        self.load_button.clicked.connect(self.load_playlist)
        self.layout.addWidget(self.load_button)

        # Scroll area to display the list of videos
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.video_list_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

        # Download selected videos button
        self.download_button = QPushButton("Download Selected Videos")
        self.download_button.clicked.connect(self.download_selected_videos)
        self.download_button.setEnabled(False)  # Disable until videos are loaded
        self.layout.addWidget(self.download_button)

        self.setLayout(self.layout)

        # Initialize the playlist data and video checkboxes
        self.playlist_data = None
        self.video_checkboxes = []

    def load_playlist(self):
        """Load the playlist from the URL without downloading."""
        playlist_url = self.url_label.text()

        if not playlist_url:
            QMessageBox.warning(self, "Input Error", "Please enter a valid playlist URL.")
            return

        try:
            ydl_opts = {
                'extract_flat': True,  # Load playlist without downloading
                'quiet': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.playlist_data = ydl.extract_info(playlist_url, download=False)

            if 'entries' in self.playlist_data:
                self.display_playlist_videos()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load playlist: {str(e)}")

    def display_playlist_videos(self):
        """Display the playlist videos with checkboxes."""
        self.video_checkboxes = []

        # Clear the previous video list
        for i in reversed(range(self.video_list_layout.count())):
            widget_to_remove = self.video_list_layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)

        # Display video entries from the playlist
        for index, entry in enumerate(self.playlist_data['entries']):
            title = entry.get('title', f"Video {index + 1}")
            video_checkbox = QCheckBox(title)
            self.video_list_layout.addWidget(video_checkbox)
            self.video_checkboxes.append((video_checkbox, entry))

        # Enable the download button after displaying the videos
        self.download_button.setEnabled(True)

    def download_selected_videos(self):
        """Download the selected videos."""
        selected_videos = [entry for checkbox, entry in self.video_checkboxes if checkbox.isChecked()]

        if not selected_videos:
            QMessageBox.warning(self, "No Selection", "Please select at least one video to download.")
            return

        self.download_videos(selected_videos)

    def download_videos(self, selected_videos):
        """Download the selected videos using yt-dlp."""
        progress_dialog = QDialog(self)
        progress_dialog.setWindowTitle("Downloading Videos")
        progress_layout = QVBoxLayout(progress_dialog)
        progress_bar = QProgressBar(progress_dialog)
        progress_layout.addWidget(progress_bar)

        progress_dialog.setLayout(progress_layout)
        progress_dialog.show()

        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'progress_hooks': [lambda d: self.update_progress(d, progress_bar)]
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                for video in selected_videos:
                    ydl.download([video['url']])

            QMessageBox.information(self, "Download Complete", "Selected videos have been downloaded.")
        except Exception as e:
            QMessageBox.critical(self, "Download Error", f"Failed to download videos: {str(e)}")
        finally:
            progress_dialog.close()

    def update_progress(self, data, progress_bar):
        """Update the progress bar during the download."""
        if data['status'] == 'downloading':
            progress_bar.setValue(int(float(data.get('downloaded_bytes', 0)) / float(data.get('total_bytes', 1)) * 100))
        elif data['status'] == 'finished':
            progress_bar.setValue(100)

class YTDLPApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("yt-dlp GUI - Lovsan's Toolbox")
        self.setGeometry(100, 100, 800, 600)

        self.setWindowIcon(QIcon("icons/app.png"))

        self.tabs = QTabWidget()
        self.settings_tab = SettingsTab()
        self.download_manager = DownloadsManager(self.settings_tab, self)  # Pass settings tab
        self.logs_tab = LogsTab()  # For download and error logs
        self.history_tab = self.download_manager.history_tab  # New downloads history tab
        self.download_later_tab = self.download_manager.download_later_tab  # Download Later tab
        self.uploads_tab = self.download_manager.uploads_tab  # Uploads tab
        self.batch_downloader_tab = BatchDownloader(self.settings_tab)  # download all links in a file
        self.editor_tab = EditorTab()  # edit files inside the app.

        # Add the tabs to the main window
        self.tabs.addTab(self.download_manager, "Downloads")
        self.tabs.addTab(self.batch_downloader_tab, "Batch Downloader")  # download all links in a file
        self.tabs.addTab(self.history_tab, "Download History")
        self.tabs.addTab(self.download_later_tab, "Download Later")
        self.tabs.addTab(self.uploads_tab, "Uploads")
        self.tabs.addTab(self.settings_tab, "Settings")
        self.tabs.addTab(self.logs_tab, "Logs")  # Add Logs tab
        self.tabs.addTab(self.editor_tab, "Editor")  # Add this line
        self.tabs.addTab(AboutTab(), "About")

        self.setCentralWidget(self.tabs)

        # Apply default theme
        self.apply_theme_on_startup()

        # Initialize and start the clipboard monitor
        self.clipboard_monitor = ClipboardMonitor()
        self.clipboard_monitor.new_url_found.connect(self.handle_new_clipboard_url)
        self.clipboard_monitor.start()

        # Add system statistics
        self.init_system_statistics()

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
        #sort these
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
        self.network_label.setText(f"Network Usage: {sent_bytes:.2f} KB/s sent, {recv_bytes:.2f} KB/s received")

        # Update active downloads
        active_downloads = self.get_active_download_count()
        self.active_downloads_label.setText(f"Active Downloads: {active_downloads}")

    def get_active_download_count(self):
        """Returns the number of active downloads."""
        # You can implement logic to track active downloads based on your current download manager
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
            with open(settings_path, "r") as f:
                settings = json.load(f)
                theme = settings.get("themes", "Grey, White, Black")
                self.apply_theme("Black and Orange")
                #force theme during dev
                #self.apply_theme(theme)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YTDLPApp()
    window.show()
    sys.exit(app.exec_())


