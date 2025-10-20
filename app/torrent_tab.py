import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QFileDialog, QProgressBar, QMessageBox, QTextEdit, QGroupBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QSplitter
)
from PyQt5.QtCore import QThread, Qt
from app.torrent_worker import TorrentWorker


class TorrentTab(QWidget):
    """Tab for downloading and managing torrents."""
    
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.worker = None
        self.thread = None
        
        # Set default download folder
        self.output_folder = os.path.join(os.getcwd(), "Downloads", "Torrents")
        os.makedirs(self.output_folder, exist_ok=True)
        
        # Create UI
        self.create_input_section()
        self.create_info_section()
        self.create_progress_section()
        self.create_output_section()
        
        self.setLayout(self.layout)
    
    def create_input_section(self):
        """Create the input section for magnet links or torrent files."""
        input_group = QGroupBox("Torrent Source")
        input_layout = QVBoxLayout()
        
        # Magnet link / torrent URL input
        magnet_layout = QHBoxLayout()
        self.magnet_label = QLabel("Magnet Link:")
        self.magnet_input = QLineEdit()
        self.magnet_input.setPlaceholderText("magnet:?xt=urn:btih:...")
        magnet_layout.addWidget(self.magnet_label)
        magnet_layout.addWidget(self.magnet_input)
        
        # File selection
        file_layout = QHBoxLayout()
        self.file_label = QLabel("Or select .torrent file:")
        self.file_path_input = QLineEdit()
        self.file_path_input.setReadOnly(True)
        self.file_path_input.setPlaceholderText("No file selected")
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_torrent_file)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_path_input)
        file_layout.addWidget(self.browse_button)
        
        # Output folder selection
        folder_layout = QHBoxLayout()
        self.folder_label = QLabel("Download Folder:")
        self.folder_path_input = QLineEdit()
        self.folder_path_input.setText(self.output_folder)
        self.folder_path_input.setReadOnly(True)
        self.select_folder_button = QPushButton("Select Folder")
        self.select_folder_button.clicked.connect(self.select_output_folder)
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.folder_path_input)
        folder_layout.addWidget(self.select_folder_button)
        
        # Action buttons
        button_layout = QHBoxLayout()
        self.download_button = QPushButton("Start Download")
        self.download_button.clicked.connect(self.start_download)
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_download)
        button_layout.addWidget(self.download_button)
        button_layout.addWidget(self.stop_button)
        
        input_layout.addLayout(magnet_layout)
        input_layout.addLayout(file_layout)
        input_layout.addLayout(folder_layout)
        input_layout.addLayout(button_layout)
        
        input_group.setLayout(input_layout)
        self.layout.addWidget(input_group)
    
    def create_info_section(self):
        """Create the torrent information display section."""
        info_group = QGroupBox("Torrent Information")
        info_layout = QVBoxLayout()
        
        # Basic info labels
        self.name_label = QLabel("Name: -")
        self.size_label = QLabel("Total Size: -")
        self.files_label = QLabel("Files: -")
        self.creator_label = QLabel("Creator: -")
        self.creation_date_label = QLabel("Created: -")
        
        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.size_label)
        info_layout.addWidget(self.files_label)
        info_layout.addWidget(self.creator_label)
        info_layout.addWidget(self.creation_date_label)
        
        # File list table
        self.files_table = QTableWidget()
        self.files_table.setColumnCount(2)
        self.files_table.setHorizontalHeaderLabels(["File Name", "Size"])
        self.files_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.files_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.files_table.setMaximumHeight(150)
        
        info_layout.addWidget(QLabel("Files:"))
        info_layout.addWidget(self.files_table)
        
        info_group.setLayout(info_layout)
        self.layout.addWidget(info_group)
    
    def create_progress_section(self):
        """Create the download progress section."""
        progress_group = QGroupBox("Download Progress")
        progress_layout = QVBoxLayout()
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        
        # Status labels
        status_layout = QHBoxLayout()
        self.speed_label = QLabel("↓ 0 KB/s | ↑ 0 KB/s")
        self.peers_label = QLabel("Peers: 0 | Seeds: 0")
        self.state_label = QLabel("State: Idle")
        status_layout.addWidget(self.speed_label)
        status_layout.addWidget(self.peers_label)
        status_layout.addWidget(self.state_label)
        status_layout.addStretch()
        
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addLayout(status_layout)
        
        progress_group.setLayout(progress_layout)
        self.layout.addWidget(progress_group)
    
    def create_output_section(self):
        """Create the output/log section."""
        output_group = QGroupBox("Status Log")
        output_layout = QVBoxLayout()
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMaximumHeight(150)
        
        output_layout.addWidget(self.output_text)
        output_group.setLayout(output_layout)
        self.layout.addWidget(output_group)
    
    def browse_torrent_file(self):
        """Open file dialog to select a .torrent file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Torrent File", "", "Torrent Files (*.torrent)"
        )
        if file_path:
            self.file_path_input.setText(file_path)
            self.magnet_input.clear()  # Clear magnet input if file is selected
    
    def select_output_folder(self):
        """Open folder dialog to select output directory."""
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder:
            self.output_folder = folder
            self.folder_path_input.setText(folder)
    
    def start_download(self):
        """Start downloading the torrent."""
        # Get torrent source
        torrent_source = self.magnet_input.text().strip()
        if not torrent_source:
            torrent_source = self.file_path_input.text().strip()
        
        if not torrent_source:
            QMessageBox.warning(self, "Input Error", "Please enter a magnet link or select a torrent file.")
            return
        
        # Validate input
        if not torrent_source.startswith('magnet:') and not os.path.isfile(torrent_source):
            QMessageBox.warning(self, "Input Error", "Invalid magnet link or torrent file path.")
            return
        
        # Reset UI
        self.progress_bar.setValue(0)
        self.output_text.clear()
        self.clear_torrent_info()
        
        # Create worker and thread
        self.thread = QThread()
        self.worker = TorrentWorker(torrent_source, self.output_folder)
        self.worker.moveToThread(self.thread)
        
        # Connect signals
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.torrent_info_received.connect(self.display_torrent_info)
        self.worker.torrent_finished.connect(self.on_download_complete)
        self.worker.torrent_failed.connect(self.on_download_failed)
        self.worker.output_received.connect(self.append_output)
        
        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.thread.deleteLater)
        
        # Update button states
        self.download_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        
        # Start download
        self.thread.start()
        self.append_output("Starting torrent download...")
    
    def stop_download(self):
        """Stop the current torrent download."""
        if self.worker:
            self.worker.stop()
            self.append_output("Stopping download...")
        
        if self.thread and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
        
        self.download_button.setEnabled(True)
        self.stop_button.setEnabled(False)
    
    def update_progress(self, progress_info):
        """Update progress bar and status labels."""
        self.progress_bar.setValue(int(progress_info['percent']))
        
        download_speed = progress_info['download_rate']
        upload_speed = progress_info['upload_rate']
        self.speed_label.setText(f"↓ {download_speed:.1f} KB/s | ↑ {upload_speed:.1f} KB/s")
        
        peers = progress_info['peers']
        seeds = progress_info['seeds']
        self.peers_label.setText(f"Peers: {peers} | Seeds: {seeds}")
        
        state = progress_info['state']
        self.state_label.setText(f"State: {state}")
    
    def display_torrent_info(self, info):
        """Display torrent information in the UI."""
        self.name_label.setText(f"Name: {info.get('name', 'Unknown')}")
        self.size_label.setText(f"Total Size: {info.get('total_size_str', '0 B')}")
        self.files_label.setText(f"Files: {info.get('num_files', 0)}")
        self.creator_label.setText(f"Creator: {info.get('creator', 'Unknown')}")
        self.creation_date_label.setText(f"Created: {info.get('creation_date', 'Unknown')}")
        
        # Populate files table
        files = info.get('files', [])
        self.files_table.setRowCount(len(files))
        for i, file_info in enumerate(files):
            self.files_table.setItem(i, 0, QTableWidgetItem(file_info['path']))
            self.files_table.setItem(i, 1, QTableWidgetItem(file_info['size_str']))
    
    def clear_torrent_info(self):
        """Clear torrent information display."""
        self.name_label.setText("Name: -")
        self.size_label.setText("Total Size: -")
        self.files_label.setText("Files: -")
        self.creator_label.setText("Creator: -")
        self.creation_date_label.setText("Created: -")
        self.files_table.setRowCount(0)
    
    def append_output(self, text):
        """Append text to the output log."""
        self.output_text.append(text)
    
    def on_download_complete(self, save_path):
        """Handle download completion."""
        self.append_output(f"Download complete! Saved to: {save_path}")
        QMessageBox.information(self, "Download Complete", f"Torrent downloaded successfully!\n\nSaved to:\n{save_path}")
        
        self.download_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        if self.thread:
            self.thread.quit()
    
    def on_download_failed(self, error_message):
        """Handle download failure."""
        self.append_output(f"Error: {error_message}")
        QMessageBox.critical(self, "Download Failed", error_message)
        
        self.download_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        if self.thread:
            self.thread.quit()
