"""
Pro Features Tab - displays Pro trial, payment options, and platform support.
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from app.trial_banner_widget import TrialBannerWidget
from app.platform_icons_widget import PlatformIconsWidget
from app.payment_widget import PaymentWidget


class ProFeaturesTab(QWidget):
    """Tab showing Pro features, trial offer, and payment options."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        # Use scroll area for better layout on small screens
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Main content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(20)
        
        # Add trial banner at the top
        self.trial_banner = TrialBannerWidget()
        content_layout.addWidget(self.trial_banner)
        
        # Add platform icons section
        self.platform_icons = PlatformIconsWidget()
        content_layout.addWidget(self.platform_icons)
        
        # Add payment widget
        self.payment_widget = PaymentWidget()
        content_layout.addWidget(self.payment_widget)
        
        # Add stretch at the bottom
        content_layout.addStretch()
        
        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)
        
        self.setLayout(main_layout)


if __name__ == "__main__":
    # Test the tab
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    tab = ProFeaturesTab()
    tab.setWindowTitle("Pro Features Test")
    tab.resize(800, 600)
    tab.show()
    sys.exit(app.exec_())
