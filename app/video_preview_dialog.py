"""
Video Preview and Trim Dialog - allows users to preview and trim videos.
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSlider, QSpinBox, QProgressBar, QMessageBox, QFileDialog,
    QGroupBox, QRadioButton, QButtonGroup
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QProcess
from PyQt5.QtGui import QFont
import os
import subprocess
import json
import requests


class TrimWorker(QThread):
    """Worker thread for video trimming operations."""
    
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)  # success, message/output_path
    
    def __init__(self, input_path, output_path, start_time, end_time, parent=None):
        super().__init__(parent)
        self.input_path = input_path
        self.output_path = output_path
        self.start_time = start_time
        self.end_time = end_time
    
    def run(self):
        """Run the trimming operation."""
        try:
            duration = self.end_time - self.start_time
            
            # Build ffmpeg command
            cmd = [
                'ffmpeg',
                '-i', self.input_path,
                '-ss', str(self.start_time),
                '-t', str(duration),
                '-c', 'copy',  # Use copy codec for fast trimming
                '-y',  # Overwrite output file
                self.output_path
            ]
            
            # Run ffmpeg
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Monitor progress (ffmpeg outputs to stderr)
            for line in process.stderr:
                # Parse progress if possible
                if 'time=' in line:
                    # Simple progress estimation
                    pass
            
            process.wait()
            
            if process.returncode == 0 and os.path.exists(self.output_path):
                self.finished.emit(True, self.output_path)
            else:
                error_msg = process.stderr.read() if process.stderr else "Unknown error"
                self.finished.emit(False, f"FFmpeg error: {error_msg}")
        
        except Exception as e:
            self.finished.emit(False, str(e))


class VideoPreviewDialog(QDialog):
    """Dialog for previewing and trimming videos."""
    
    def __init__(self, video_path=None, video_url=None, video_duration=None, parent=None):
        super().__init__(parent)
        self.video_path = video_path
        self.video_url = video_url
        self.video_duration = video_duration or 0
        self.trim_worker = None
        
        self.setWindowTitle("Video Preview & Trim")
        self.setMinimumSize(800, 600)
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("Video Preview & Trimming Tool")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Video info
        info_group = QGroupBox("Video Information")
        info_layout = QVBoxLayout()
        
        if self.video_path:
            self.video_info_label = QLabel(f"<b>File:</b> {os.path.basename(self.video_path)}")
        elif self.video_url:
            self.video_info_label = QLabel(f"<b>URL:</b> {self.video_url}")
        else:
            self.video_info_label = QLabel("<b>No video loaded</b>")
        
        self.video_info_label.setWordWrap(True)
        info_layout.addWidget(self.video_info_label)
        
        # Duration info
        self.duration_label = QLabel(f"<b>Duration:</b> {self.format_time(self.video_duration)}")
        info_layout.addWidget(self.duration_label)
        
        info_group.setLayout(info_layout)
        main_layout.addWidget(info_group)
        
        # Preview placeholder
        preview_group = QGroupBox("Video Preview")
        preview_layout = QVBoxLayout()
        
        self.preview_label = QLabel("🎬 Video Preview Placeholder")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("""
            QLabel {
                background-color: #000;
                color: #fff;
                font-size: 16px;
                min-height: 300px;
                border: 2px solid #666;
            }
        """)
        preview_layout.addWidget(self.preview_label)
        
        # Playback controls
        controls_layout = QHBoxLayout()
        
        self.play_button = QPushButton("▶ Play")
        self.play_button.clicked.connect(self.play_video)
        controls_layout.addWidget(self.play_button)
        
        self.pause_button = QPushButton("⏸ Pause")
        self.pause_button.setEnabled(False)
        controls_layout.addWidget(self.pause_button)
        
        self.stop_button = QPushButton("⏹ Stop")
        self.stop_button.setEnabled(False)
        controls_layout.addWidget(self.stop_button)
        
        preview_layout.addLayout(controls_layout)
        
        # Note about native player
        note_label = QLabel(
            "💡 <i>Note: Full video preview will open in your system's default media player. "
            "Use the trimming controls below to select a segment.</i>"
        )
        note_label.setWordWrap(True)
        note_label.setStyleSheet("color: #666; font-size: 11px;")
        preview_layout.addWidget(note_label)
        
        preview_group.setLayout(preview_layout)
        main_layout.addWidget(preview_group)
        
        # Trimming controls
        trim_group = QGroupBox("Trimming Controls")
        trim_layout = QVBoxLayout()
        
        # Start time
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("Start Time (seconds):"))
        self.start_time_spin = QSpinBox()
        self.start_time_spin.setRange(0, int(self.video_duration) if self.video_duration else 3600)
        self.start_time_spin.setValue(0)
        self.start_time_spin.valueChanged.connect(self.update_duration_preview)
        start_layout.addWidget(self.start_time_spin)
        self.start_time_label = QLabel("00:00:00")
        start_layout.addWidget(self.start_time_label)
        start_layout.addStretch()
        trim_layout.addLayout(start_layout)
        
        # End time
        end_layout = QHBoxLayout()
        end_layout.addWidget(QLabel("End Time (seconds):"))
        self.end_time_spin = QSpinBox()
        self.end_time_spin.setRange(0, int(self.video_duration) if self.video_duration else 3600)
        self.end_time_spin.setValue(int(self.video_duration) if self.video_duration else 60)
        self.end_time_spin.valueChanged.connect(self.update_duration_preview)
        end_layout.addWidget(self.end_time_spin)
        self.end_time_label = QLabel(self.format_time(self.video_duration))
        end_layout.addWidget(self.end_time_label)
        end_layout.addStretch()
        trim_layout.addLayout(end_layout)
        
        # Trim duration preview
        self.trim_duration_label = QLabel()
        self.trim_duration_label.setStyleSheet("font-weight: bold; color: #4CAF50;")
        self.update_duration_preview()
        trim_layout.addWidget(self.trim_duration_label)
        
        trim_group.setLayout(trim_layout)
        main_layout.addWidget(trim_group)
        
        # Trimming mode selection
        mode_group = QGroupBox("Trimming Mode")
        mode_layout = QVBoxLayout()
        
        self.mode_button_group = QButtonGroup()
        
        self.local_mode_radio = QRadioButton("Local (FFmpeg) - Fast, requires downloaded video file")
        self.local_mode_radio.setChecked(True)
        self.mode_button_group.addButton(self.local_mode_radio)
        mode_layout.addWidget(self.local_mode_radio)
        
        self.server_mode_radio = QRadioButton("Server-side - Requires server API, works with URLs")
        self.mode_button_group.addButton(self.server_mode_radio)
        mode_layout.addWidget(self.server_mode_radio)
        
        mode_group.setLayout(mode_layout)
        main_layout.addWidget(mode_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #666; font-style: italic;")
        main_layout.addWidget(self.status_label)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        self.trim_button = QPushButton("✂️ Trim Video")
        self.trim_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.trim_button.clicked.connect(self.trim_video)
        buttons_layout.addWidget(self.trim_button)
        
        self.download_button = QPushButton("💾 Download Trimmed")
        self.download_button.setEnabled(False)
        buttons_layout.addWidget(self.download_button)
        
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.accept)
        buttons_layout.addWidget(self.close_button)
        
        main_layout.addLayout(buttons_layout)
        
        self.setLayout(main_layout)
    
    def format_time(self, seconds):
        """Format seconds as HH:MM:SS."""
        if not seconds:
            return "00:00:00"
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def update_duration_preview(self):
        """Update the trim duration preview."""
        start = self.start_time_spin.value()
        end = self.end_time_spin.value()
        
        # Update time labels
        self.start_time_label.setText(self.format_time(start))
        self.end_time_label.setText(self.format_time(end))
        
        # Calculate and display trim duration
        if end > start:
            duration = end - start
            self.trim_duration_label.setText(
                f"Trimmed duration: {self.format_time(duration)}"
            )
            self.trim_button.setEnabled(True)
        else:
            self.trim_duration_label.setText("⚠️ End time must be greater than start time")
            self.trim_button.setEnabled(False)
    
    def play_video(self):
        """Play the video in system player."""
        if self.video_path and os.path.exists(self.video_path):
            # Open in default player
            import platform
            system = platform.system()
            
            try:
                if system == 'Windows':
                    os.startfile(self.video_path)
                elif system == 'Darwin':  # macOS
                    subprocess.call(['open', self.video_path])
                else:  # Linux
                    subprocess.call(['xdg-open', self.video_path])
                
                self.status_label.setText("✓ Video opened in system player")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not open video: {str(e)}")
        else:
            QMessageBox.information(
                self,
                "No Local File",
                "Video preview requires a downloaded file. Download the video first to preview it."
            )
    
    def trim_video(self):
        """Trim the video based on selected times."""
        start = self.start_time_spin.value()
        end = self.end_time_spin.value()
        
        if end <= start:
            QMessageBox.warning(self, "Invalid Range", "End time must be greater than start time.")
            return
        
        if self.local_mode_radio.isChecked():
            self.trim_local(start, end)
        else:
            self.trim_server_side(start, end)
    
    def trim_local(self, start, end):
        """Trim video locally using FFmpeg."""
        if not self.video_path or not os.path.exists(self.video_path):
            QMessageBox.warning(
                self,
                "No Local File",
                "Local trimming requires a downloaded video file. Please download the video first."
            )
            return
        
        # Check if ffmpeg is available
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            QMessageBox.warning(
                self,
                "FFmpeg Not Found",
                "FFmpeg is required for video trimming but was not found on your system.\n\n"
                "Please install FFmpeg or use server-side trimming mode."
            )
            return
        
        # Choose output file
        base_name = os.path.splitext(os.path.basename(self.video_path))[0]
        ext = os.path.splitext(self.video_path)[1]
        default_name = f"{base_name}_trimmed{ext}"
        
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Trimmed Video",
            default_name,
            f"Video Files (*{ext});;All Files (*.*)"
        )
        
        if not output_path:
            return
        
        # Start trimming
        self.trim_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.status_label.setText("Trimming video... This may take a moment.")
        
        self.trim_worker = TrimWorker(self.video_path, output_path, start, end)
        self.trim_worker.progress.connect(self.on_trim_progress)
        self.trim_worker.finished.connect(self.on_trim_finished)
        self.trim_worker.start()
    
    def trim_server_side(self, start, end):
        """Trim video on server."""
        server_url = os.environ.get('UVDM_LICENSE_SERVER')
        if not server_url:
            QMessageBox.information(
                self,
                "Server Not Configured",
                "Server-side trimming requires the API server to be configured.\n\n"
                "Set the UVDM_LICENSE_SERVER environment variable and ensure the API server is running.\n\n"
                "See README.md for configuration instructions."
            )
            return
        
        # Prepare request
        source = self.video_url if self.video_url else self.video_path
        
        self.trim_button.setEnabled(False)
        self.status_label.setText("Submitting trim job to server...")
        
        try:
            response = requests.post(
                f"{server_url}/api/trim",
                json={
                    'source': source,
                    'start': start,
                    'end': end
                },
                timeout=10
            )
            
            if response.status_code == 501:
                QMessageBox.information(
                    self,
                    "Not Implemented",
                    "Server-side trimming is not yet implemented on the API server.\n\n"
                    "This is a placeholder endpoint. Use local trimming mode or wait for server implementation."
                )
            elif response.status_code == 200:
                result = response.json()
                QMessageBox.information(
                    self,
                    "Success",
                    f"Trim job submitted successfully!\n\nJob ID: {result.get('job_id', 'N/A')}"
                )
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Server returned error: {response.status_code}\n{response.text}"
                )
        
        except requests.exceptions.Timeout:
            QMessageBox.warning(self, "Timeout", "Server request timed out.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Request failed: {str(e)}")
        
        finally:
            self.trim_button.setEnabled(True)
            self.status_label.setText("")
    
    def on_trim_progress(self, value):
        """Handle trim progress update."""
        self.progress_bar.setValue(value)
    
    def on_trim_finished(self, success, message):
        """Handle trim completion."""
        self.progress_bar.setVisible(False)
        self.trim_button.setEnabled(True)
        
        if success:
            self.status_label.setText(f"✓ Video trimmed successfully!")
            self.download_button.setEnabled(True)
            
            QMessageBox.information(
                self,
                "Success",
                f"Video trimmed successfully!\n\nSaved to:\n{message}"
            )
        else:
            self.status_label.setText(f"✗ Trimming failed")
            QMessageBox.warning(
                self,
                "Trimming Failed",
                f"Failed to trim video:\n\n{message}"
            )


if __name__ == "__main__":
    # Test the dialog
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Example with a test video file
    dialog = VideoPreviewDialog(
        video_path="/path/to/test/video.mp4",
        video_duration=120
    )
    dialog.exec_()
