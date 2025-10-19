"""
Platform Icons Widget - displays supported platforms with icons and help dialogs.
"""
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QPushButton, QMessageBox, 
    QVBoxLayout, QDialog, QTextEdit, QGroupBox
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtSvg import QSvgWidget
import os


class PlatformHelpDialog(QDialog):
    """Dialog showing platform-specific information."""
    
    def __init__(self, platform_name, platform_info, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{platform_name} - Platform Information")
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout()
        
        # Platform name header
        header = QLabel(f"<h2>{platform_name}</h2>")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Platform information
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setHtml(platform_info)
        layout.addWidget(info_text)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)


class PlatformIconButton(QPushButton):
    """Custom button for platform icons with hover effects."""
    
    def __init__(self, icon_path, platform_name, platform_info, parent=None):
        super().__init__(parent)
        self.platform_name = platform_name
        self.platform_info = platform_info
        
        # Set icon
        if os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(48, 48))
        
        # Set button properties
        self.setFlat(True)
        self.setToolTip(f"Click to learn more about {platform_name} support")
        self.setCursor(Qt.PointingHandCursor)
        
        # Set fixed size
        self.setFixedSize(60, 60)
        
        # Connect click event
        self.clicked.connect(self.show_platform_info)
        
        # Style
        self.setStyleSheet("""
            QPushButton {
                border: 2px solid transparent;
                border-radius: 8px;
                padding: 4px;
            }
            QPushButton:hover {
                border: 2px solid #4CAF50;
                background-color: rgba(76, 175, 80, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(76, 175, 80, 0.2);
            }
        """)
    
    def show_platform_info(self):
        """Show platform-specific help dialog."""
        dialog = PlatformHelpDialog(self.platform_name, self.platform_info, self)
        dialog.exec_()


class PlatformIconsWidget(QWidget):
    """Widget displaying supported platform icons."""
    
    PLATFORMS = [
        {
            'name': 'YouTube',
            'icon': 'assets/platform-icons/youtube.svg',
            'info': """
                <h3>YouTube Support</h3>
                <p><b>Status:</b> Fully Supported</p>
                <p><b>Features:</b></p>
                <ul>
                    <li>Single video downloads</li>
                    <li>Playlist downloads</li>
                    <li>Channel downloads</li>
                    <li>Multiple quality options (144p to 4K+)</li>
                    <li>Audio-only downloads (MP3, M4A, etc.)</li>
                    <li>Age-restricted content support</li>
                    <li>Subtitles/captions download</li>
                </ul>
                <p><b>Notes:</b> YouTube is the most widely tested platform with excellent support.</p>
            """
        },
        {
            'name': 'Facebook',
            'icon': 'assets/platform-icons/facebook.svg',
            'info': """
                <h3>Facebook Support</h3>
                <p><b>Status:</b> Supported</p>
                <p><b>Features:</b></p>
                <ul>
                    <li>Public video downloads</li>
                    <li>Facebook Watch support</li>
                    <li>Live video recording</li>
                    <li>Multiple quality options</li>
                </ul>
                <p><b>Notes:</b> Private videos require authentication. Some videos may have geographic restrictions.</p>
            """
        },
        {
            'name': 'Instagram',
            'icon': 'assets/platform-icons/instagram.svg',
            'info': """
                <h3>Instagram Support</h3>
                <p><b>Status:</b> Supported</p>
                <p><b>Features:</b></p>
                <ul>
                    <li>Post video downloads</li>
                    <li>Reel downloads</li>
                    <li>IGTV downloads</li>
                    <li>Story downloads (if available)</li>
                </ul>
                <p><b>Notes:</b> Private account content requires authentication. Stories may expire quickly.</p>
            """
        },
        {
            'name': 'TikTok',
            'icon': 'assets/platform-icons/tiktok.svg',
            'info': """
                <h3>TikTok Support</h3>
                <p><b>Status:</b> Supported</p>
                <p><b>Features:</b></p>
                <ul>
                    <li>Single video downloads</li>
                    <li>Downloads without watermark (when possible)</li>
                    <li>Audio extraction</li>
                </ul>
                <p><b>Notes:</b> TikTok frequently changes their API. Some videos may require updated yt-dlp version.</p>
            """
        },
        {
            'name': 'Adult Sites',
            'icon': 'assets/platform-icons/adult.svg',
            'info': """
                <h3>Adult Content Support</h3>
                <p><b>Status:</b> Supported</p>
                <p><b>Supported Sites:</b> Various adult content platforms</p>
                <p><b>Features:</b></p>
                <ul>
                    <li>Video downloads from major adult sites</li>
                    <li>Multiple quality options</li>
                    <li>Premium content support (with credentials)</li>
                </ul>
                <p><b>Notes:</b> Age verification required. Some content may require account authentication.</p>
                <p><b>⚠️ Content Warning:</b> Adult content (18+)</p>
            """
        },
        {
            'name': '1000+ More',
            'icon': 'assets/platform-icons/more.svg',
            'info': """
                <h3>Additional Platforms</h3>
                <p><b>Status:</b> 1000+ sites supported via yt-dlp</p>
                <p><b>Popular Platforms:</b></p>
                <ul>
                    <li>Twitter/X</li>
                    <li>Reddit</li>
                    <li>Vimeo</li>
                    <li>Dailymotion</li>
                    <li>Twitch</li>
                    <li>SoundCloud</li>
                    <li>And many more...</li>
                </ul>
                <p><b>View All:</b> Click "View Supported Sites" in the About tab to see the complete list.</p>
                <p><b>Notes:</b> Support varies by platform. Most major video hosting sites are supported.</p>
            """
        }
    ]
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        main_layout = QVBoxLayout()
        
        # Group box for platforms
        group_box = QGroupBox("Supported Platforms")
        group_layout = QVBoxLayout()
        
        # Title label
        title = QLabel("UVDM supports downloading from these platforms and 1000+ more:")
        title.setWordWrap(True)
        title.setAlignment(Qt.AlignCenter)
        group_layout.addWidget(title)
        
        # Icons layout
        icons_layout = QHBoxLayout()
        icons_layout.setAlignment(Qt.AlignCenter)
        icons_layout.setSpacing(15)
        
        # Create icon buttons for each platform
        for platform in self.PLATFORMS:
            icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), platform['icon'])
            
            # Container for icon and label
            icon_container = QVBoxLayout()
            icon_container.setAlignment(Qt.AlignCenter)
            
            # Icon button
            icon_btn = PlatformIconButton(icon_path, platform['name'], platform['info'])
            icon_container.addWidget(icon_btn)
            
            # Platform name label
            name_label = QLabel(platform['name'])
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setStyleSheet("font-size: 10px; color: #666;")
            icon_container.addWidget(name_label)
            
            # Add to main layout
            container_widget = QWidget()
            container_widget.setLayout(icon_container)
            icons_layout.addWidget(container_widget)
        
        group_layout.addLayout(icons_layout)
        
        # Info text
        info_label = QLabel("💡 Click on any platform icon to learn more about its support and features.")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("font-style: italic; color: #888; margin-top: 10px;")
        group_layout.addWidget(info_label)
        
        group_box.setLayout(group_layout)
        main_layout.addWidget(group_box)
        
        self.setLayout(main_layout)


if __name__ == "__main__":
    # Test the widget
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    widget = PlatformIconsWidget()
    widget.setWindowTitle("Platform Icons Test")
    widget.resize(800, 200)
    widget.show()
    sys.exit(app.exec_())
