import os
import time
import logging
from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal
import libtorrent as lt


class TorrentWorker(QObject):
    """Worker class to handle torrent downloads using libtorrent."""
    
    progress_updated = pyqtSignal(dict)  # {percent, download_rate, upload_rate, peers, seeds}
    torrent_info_received = pyqtSignal(dict)  # Torrent metadata
    torrent_finished = pyqtSignal(str)  # Download path
    torrent_failed = pyqtSignal(str)  # Error message
    output_received = pyqtSignal(str)  # Status messages
    
    def __init__(self, torrent_source, output_folder, parent=None):
        """
        Initialize torrent worker.
        
        Args:
            torrent_source: Either a magnet link or path to .torrent file
            output_folder: Directory to save downloaded files
            parent: Parent QObject
        """
        super().__init__(parent)
        self.torrent_source = torrent_source
        self.output_folder = output_folder
        self.session = None
        self.handle = None
        self.running = True
        
    def run(self):
        """Main download loop."""
        try:
            # Create libtorrent session
            self.session = lt.session({'listen_interfaces': '0.0.0.0:6881'})
            
            # Set session settings for better performance
            settings = {
                'user_agent': 'UVDM/1.0 libtorrent/' + lt.__version__,
                'enable_dht': True,
                'enable_lsd': True,
                'enable_upnp': True,
                'enable_natpmp': True,
            }
            self.session.apply_settings(settings)
            
            self.output_received.emit("Starting torrent session...")
            
            # Add torrent
            params = {
                'save_path': self.output_folder,
                'storage_mode': lt.storage_mode_t.storage_mode_sparse,
            }
            
            if self.torrent_source.startswith('magnet:'):
                # Magnet link
                self.output_received.emit("Adding magnet link...")
                self.handle = lt.add_magnet_uri(self.session, self.torrent_source, params)
            else:
                # Torrent file
                self.output_received.emit(f"Loading torrent file: {self.torrent_source}")
                info = lt.torrent_info(self.torrent_source)
                params['ti'] = info
                self.handle = self.session.add_torrent(params)
            
            self.output_received.emit("Waiting for metadata...")
            
            # Wait for metadata (important for magnet links)
            while not self.handle.has_metadata():
                time.sleep(0.1)
                if not self.running:
                    return
            
            self.output_received.emit("Metadata received, starting download...")
            
            # Get torrent info
            torrent_info = self.get_torrent_info()
            self.torrent_info_received.emit(torrent_info)
            
            # Main download loop
            while self.running:
                status = self.handle.status()
                
                # Update progress
                progress_info = {
                    'percent': status.progress * 100,
                    'download_rate': status.download_rate / 1000,  # KB/s
                    'upload_rate': status.upload_rate / 1000,  # KB/s
                    'peers': status.num_peers,
                    'seeds': status.num_seeds,
                    'state': str(status.state),
                    'total_download': status.total_download,
                    'total_upload': status.total_upload,
                }
                self.progress_updated.emit(progress_info)
                
                # Check if finished
                if status.is_seeding:
                    self.output_received.emit("Download complete! Seeding...")
                    save_path = os.path.join(self.output_folder, self.handle.name())
                    self.torrent_finished.emit(save_path)
                    break
                
                # Check for errors
                if status.error:
                    raise Exception(f"Torrent error: {status.error}")
                
                time.sleep(1)
                
        except Exception as e:
            error_msg = f"Torrent download failed: {str(e)}"
            logging.error(error_msg)
            self.torrent_failed.emit(error_msg)
        finally:
            if self.session and self.handle:
                try:
                    # Pause the torrent to allow cleanup
                    self.handle.pause()
                except:
                    pass
    
    def get_torrent_info(self):
        """Extract and return torrent information."""
        if not self.handle or not self.handle.has_metadata():
            return {}
        
        status = self.handle.status()
        torrent_file = self.handle.torrent_file()
        
        # Get file list
        files = []
        if torrent_file:
            file_storage = torrent_file.files()
            for i in range(file_storage.num_files()):
                file_path = file_storage.file_path(i)
                file_size = file_storage.file_size(i)
                files.append({
                    'path': file_path,
                    'size': file_size,
                    'size_str': self.format_size(file_size)
                })
        
        info = {
            'name': self.handle.name(),
            'total_size': torrent_file.total_size() if torrent_file else 0,
            'total_size_str': self.format_size(torrent_file.total_size() if torrent_file else 0),
            'num_files': len(files),
            'files': files,
            'num_pieces': torrent_file.num_pieces() if torrent_file else 0,
            'piece_length': torrent_file.piece_length() if torrent_file else 0,
            'creator': torrent_file.creator() if torrent_file else '',
            'comment': torrent_file.comment() if torrent_file else '',
            'creation_date': datetime.fromtimestamp(torrent_file.creation_date()).strftime('%Y-%m-%d %H:%M:%S') if torrent_file and torrent_file.creation_date() > 0 else 'Unknown',
        }
        
        return info
    
    def format_size(self, size_bytes):
        """Format bytes to human readable string."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    def stop(self):
        """Stop the torrent download."""
        self.running = False
        if self.handle:
            try:
                self.handle.pause()
            except:
                pass
