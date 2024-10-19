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



