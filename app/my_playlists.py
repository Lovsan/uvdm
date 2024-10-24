import json
import os

class PlaylistManager:
    def __init__(self, playlist_file='my_playlists.json'):
        self.playlist_file = playlist_file
        self.load_playlists()

    def load_playlists(self):
        if os.path.exists(self.playlist_file):
            with open(self.playlist_file, 'r') as file:
                self.playlists = json.load(file).get("playlists", [])
        else:
            self.playlists = []

    def save_playlists(self):
        with open(self.playlist_file, 'w') as file:
            json.dump({"playlists": self.playlists}, file, indent=4)

    def add_playlist(self, name, entries):
        self.playlists.append({"name": name, "entries": entries})
        self.save_playlists()

    def remove_playlist(self, name):
        self.playlists = [p for p in self.playlists if p['name'] != name]
        self.save_playlists()

    def rename_playlist(self, old_name, new_name):
        for playlist in self.playlists:
            if playlist['name'] == old_name:
                playlist['name'] = new_name
                self.save_playlists()
                return True
        return False

    def get_playlist(self, name):
        for playlist in self.playlists:
            if playlist['name'] == name:
                return playlist
        return None

# Example usage
#playlist_manager = PlaylistManager()
#playlist_manager.add_playlist("My Videos", [{"title": "Video 1", "path": "/path/to/video1.mp4"}])
#playlist_manager.rename_playlist("My Videos", "Favorite Videos")