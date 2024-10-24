import os
import json
import subprocess
import platform
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QMenu, QAction, QMessageBox,
    QFileDialog, QInputDialog, QDialog, QDialogButtonBox, QHBoxLayout, QPushButton, QLabel
)
from PyQt5.QtCore import Qt

class PlaylistManager:
    def __init__(self, playlists_dir='my_playlists'):
        self.playlists_dir = playlists_dir
        self.load_playlists()

    def load_playlists(self):
        """Load playlists from the specified directory."""
        if not os.path.exists(self.playlists_dir):
            os.makedirs(self.playlists_dir)
        self.playlists = []
        for filename in os.listdir(self.playlists_dir):
            if filename.endswith('.m3u8'):
                playlist_name = os.path.splitext(filename)[0]
                self.playlists.append({
                    "name": playlist_name,
                    "file": filename,
                    "entries": self.load_playlist_entries(filename)
                })

    def load_playlist_entries(self, filename):
        """Load entries from a .m3u8 playlist file."""
        entries = []
        file_path = os.path.join(self.playlists_dir, filename)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            entries.append({"title": os.path.basename(line), "path": line})
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='cp1252') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            entries.append({"title": os.path.basename(line), "path": line})
        return entries

    def save_playlist(self, name, entries):
        """Save a playlist to the .m3u8 file."""
        filename = f"{name}.m3u8"
        file_path = os.path.join(self.playlists_dir, filename)
        with open(file_path, 'w') as f:
            f.write("#EXTM3U\n")
            for entry in entries:
                f.write(f"{entry['path']}\n")
        self.load_playlists()  # Reload playlists to update the list

    def remove_playlist(self, name):
        """Delete a playlist file."""
        filename = f"{name}.m3u8"
        file_path = os.path.join(self.playlists_dir, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        self.load_playlists()

    def rename_playlist(self, old_name, new_name):
        """Rename a playlist file."""
        old_filename = f"{old_name}.m3u8"
        new_filename = f"{new_name}.m3u8"
        old_path = os.path.join(self.playlists_dir, old_filename)
        new_path = os.path.join(self.playlists_dir, new_filename)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
        self.load_playlists()

    def get_playlist(self, name):
        """Get a playlist by name."""
        for playlist in self.playlists:
            if playlist['name'] == name:
                return playlist
        return None

class MyPlaylistsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.playlist_manager = PlaylistManager()
        self.playlist_list = QListWidget()
        self.load_playlists()

        self.playlist_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.playlist_list.customContextMenuRequested.connect(self.show_context_menu)

        self.layout.addWidget(self.playlist_list)
        self.setLayout(self.layout)

    def load_playlists(self):
        """Load playlists from the playlist manager."""
        self.playlist_list.clear()
        for playlist in self.playlist_manager.playlists:
            num_songs = len(playlist['entries'])
            playlist_item = f"{playlist['name']} - {num_songs} songs"
            self.playlist_list.addItem(playlist_item)

    def show_context_menu(self, position):
        """Show the context menu for playlist actions."""
        item = self.playlist_list.itemAt(position)
        if item:
            menu = QMenu()
            open_action = QAction("Edit playlist", self)
            play_action = QAction("Play", self)
            delete_action = QAction("Delete", self)
            rename_action = QAction("Rename", self)

            open_action.triggered.connect(lambda: self.open_playlist(item))
            play_action.triggered.connect(lambda: self.play_playlist(item))
            delete_action.triggered.connect(lambda: self.delete_playlist(item))
            rename_action.triggered.connect(lambda: self.rename_playlist(item))

            menu.addAction(open_action)
            menu.addAction(play_action)
            menu.addAction(delete_action)
            menu.addAction(rename_action)
            menu.exec_(self.playlist_list.viewport().mapToGlobal(position))

    def open_playlist(self, item):
        """Open the selected playlist and show its contents in a dialog."""
        playlist_name = item.text().split(" - ")[0]
        playlist = self.playlist_manager.get_playlist(playlist_name)
        if not playlist:
            QMessageBox.warning(self, "Error", "The selected playlist could not be found.")
            return

        # Create a dialog to display the playlist contents
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Playlist: {playlist_name}")
        dialog.setLayout(QVBoxLayout())

        # List widget to show the playlist entries
        entry_list = QListWidget()
        for entry in playlist['entries']:
            entry_list.addItem(f"{entry['title']} - {entry['path']}")

        # Buttons for adding, removing, and saving entries
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Entry")
        remove_button = QPushButton("Remove Selected")
        save_button = QPushButton("Save Playlist")
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        button_layout.addWidget(save_button)

        # Connect button actions
        add_button.clicked.connect(lambda: self.add_entry_to_playlist(entry_list))
        remove_button.clicked.connect(lambda: self.remove_selected_entry(entry_list))
        save_button.clicked.connect(lambda: self.save_playlist_changes(playlist_name, entry_list))

        # Add widgets to the dialog layout
        dialog.layout().addWidget(entry_list)
        dialog.layout().addLayout(button_layout)
        dialog.exec_()

    def play_playlist(self, item):
        """Play all entries in the selected playlist using the system's default media player."""
        playlist_name = item.text().split(" - ")[0]
        playlist = self.playlist_manager.get_playlist(playlist_name)
        if not playlist or not playlist['entries']:
            QMessageBox.warning(self, "Error", "The selected playlist is empty or could not be found.")
            return

        # Play each entry in the playlist
        for entry in playlist['entries']:
            self.play_entry(entry['path'])

    def play_entry(self, path):
        """Play the selected entry using the system's default media player."""
        if os.path.exists(path):
            try:
                if platform.system() == "Windows":
                    os.startfile(path)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.call(["open", path])
                else:  # Linux and other Unix-like systems
                    subprocess.call(["xdg-open", path])
            except Exception as e:
                QMessageBox.critical(self, "Play Error", f"An error occurred while trying to play the file: {str(e)}")
        else:
            QMessageBox.warning(self, "File Not Found", "The file could not be found.")

    def delete_playlist(self, item):
        """Delete the selected playlist."""
        playlist_name = item.text().split(" - ")[0]
        confirm = QMessageBox.question(self, "Delete Playlist", f"Are you sure you want to delete '{playlist_name}'?")
        if confirm == QMessageBox.Yes:
            self.playlist_manager.remove_playlist(playlist_name)
            self.load_playlists()
            QMessageBox.information(self, "Deleted", f"The playlist '{playlist_name}' has been deleted.")

    def rename_playlist(self, item):
        """Rename the selected playlist."""
        old_name = item.text().split(" - ")[0]
        new_name, ok = QInputDialog.getText(self, "Rename Playlist", "Enter new name:")
        if ok and new_name:
            self.playlist_manager.rename_playlist(old_name, new_name)
            self.load_playlists()
            QMessageBox.information(self, "Renamed", f"The playlist has been renamed to '{new_name}'.")

    def add_entry_to_playlist(self, entry_list):
        """Add a new entry to the selected playlist."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Add")
        if file_path:
            title = os.path.basename(file_path)
            entry_list.addItem(f"{title} - {file_path}")

    def remove_selected_entry(self, entry_list):
        """Remove the selected entry from the playlist."""
        selected_items = entry_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select an entry to remove.")
            return
        for item in selected_items:
            entry_list.takeItem(entry_list.row(item))

    def save_playlist_changes(self, playlist_name, entry_list):
        """Save the changes made to the playlist."""
        entries = []
        for i in range(entry_list.count()):
            text = entry_list.item(i).text()
            # Ensure that the text format is correct before splitting
            if " - " in text:
                title, path = text.split(" - ", 1)
                entries.append({"title": title, "path": path})
            else:
                # If the format is not as expected, skip this entry
                continue

        # Save the updated playlist entries
        if entries:
            self.playlist_manager.save_playlist(playlist_name, entries)
            QMessageBox.information(self, "Saved", "The playlist changes have been saved.")
        else:
            QMessageBox.warning(self, "Empty Playlist", "The playlist is empty or invalid. No changes were saved.")
