"""
Trial Banner Widget - offers 2-week free Pro trial for first-time users.
"""
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, 
    QMessageBox, QFrame
)
from PyQt5.QtCore import Qt, QSettings, QDateTime, QTimer
from PyQt5.QtGui import QFont
import requests
import os


class TrialBannerWidget(QWidget):
    """Widget displaying free trial offer and status."""
    
    TRIAL_DURATION_DAYS = 14
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings('UVDM', 'TrialManager')
        self.init_ui()
        self.update_trial_status()
        
        # Update trial status every minute
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_trial_status)
        self.timer.start(60000)  # 60 seconds
    
    def init_ui(self):
        """Initialize the UI."""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create a frame for the banner
        self.banner_frame = QFrame()
        self.banner_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.banner_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4CAF50, stop:1 #2196F3);
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        banner_layout = QHBoxLayout()
        
        # Icon/Badge
        badge_label = QLabel("🎁")
        badge_label.setStyleSheet("font-size: 32px;")
        banner_layout.addWidget(badge_label)
        
        # Text content
        text_layout = QVBoxLayout()
        
        self.title_label = QLabel("Get 2 Weeks of Pro Features Free!")
        self.title_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        text_layout.addWidget(self.title_label)
        
        self.subtitle_label = QLabel("First-time users can try all Pro features with no credit card required")
        self.subtitle_label.setStyleSheet("color: white; font-size: 12px;")
        self.subtitle_label.setWordWrap(True)
        text_layout.addWidget(self.subtitle_label)
        
        banner_layout.addLayout(text_layout, 1)
        
        # Action button
        self.action_button = QPushButton("Claim Free Trial")
        self.action_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #4CAF50;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #888888;
            }
        """)
        self.action_button.clicked.connect(self.claim_trial)
        banner_layout.addWidget(self.action_button)
        
        self.banner_frame.setLayout(banner_layout)
        main_layout.addWidget(self.banner_frame)
        
        self.setLayout(main_layout)
    
    def is_trial_active(self):
        """Check if trial is currently active."""
        trial_claimed = self.settings.value('trial_claimed', False, type=bool)
        if not trial_claimed:
            return False
        
        expires_str = self.settings.value('trial_expires_at', '')
        if not expires_str:
            return False
        
        expires_at = QDateTime.fromString(expires_str, Qt.ISODate)
        return QDateTime.currentDateTime() < expires_at
    
    def get_trial_remaining(self):
        """Get remaining trial time in days and hours."""
        expires_str = self.settings.value('trial_expires_at', '')
        if not expires_str:
            return None
        
        expires_at = QDateTime.fromString(expires_str, Qt.ISODate)
        current = QDateTime.currentDateTime()
        
        if current >= expires_at:
            return None
        
        seconds_remaining = current.secsTo(expires_at)
        days = seconds_remaining // 86400
        hours = (seconds_remaining % 86400) // 3600
        
        return {'days': days, 'hours': hours}
    
    def update_trial_status(self):
        """Update the banner based on trial status."""
        trial_claimed = self.settings.value('trial_claimed', False, type=bool)
        
        if not trial_claimed:
            # Show claim offer
            self.title_label.setText("Get 2 Weeks of Pro Features Free!")
            self.subtitle_label.setText("First-time users can try all Pro features with no credit card required")
            self.action_button.setText("Claim Free Trial")
            self.action_button.setEnabled(True)
            self.banner_frame.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4CAF50, stop:1 #2196F3);
                    border-radius: 8px;
                    padding: 10px;
                }
            """)
        elif self.is_trial_active():
            # Show active trial status
            remaining = self.get_trial_remaining()
            if remaining:
                if remaining['days'] > 0:
                    time_str = f"{remaining['days']} days, {remaining['hours']} hours"
                else:
                    time_str = f"{remaining['hours']} hours"
                
                self.title_label.setText(f"Pro Trial Active - {time_str} remaining")
                self.subtitle_label.setText("Enjoying Pro features? Subscribe to keep them after trial ends")
                self.action_button.setText("View Plans")
                self.action_button.setEnabled(True)
                self.banner_frame.setStyleSheet("""
                    QFrame {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                            stop:0 #2196F3, stop:1 #1976D2);
                        border-radius: 8px;
                        padding: 10px;
                    }
                """)
        else:
            # Trial expired
            self.title_label.setText("Free Trial Expired")
            self.subtitle_label.setText("Subscribe to Pro to continue using advanced features")
            self.action_button.setText("View Plans")
            self.action_button.setEnabled(True)
            self.banner_frame.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #FF9800, stop:1 #F57C00);
                    border-radius: 8px;
                    padding: 10px;
                }
            """)
    
    def claim_trial(self):
        """Claim the free trial."""
        trial_claimed = self.settings.value('trial_claimed', False, type=bool)
        
        if trial_claimed and self.is_trial_active():
            # Show subscription plans
            QMessageBox.information(
                self,
                "Pro Subscription",
                "Subscription plans will be available here.\n\n"
                "This is a placeholder for the payment integration."
            )
            return
        
        if trial_claimed and not self.is_trial_active():
            # Trial expired, show plans
            QMessageBox.information(
                self,
                "Pro Subscription",
                "Your free trial has expired.\n\n"
                "Subscription plans will be available here.\n"
                "This is a placeholder for the payment integration."
            )
            return
        
        # Confirm trial claim
        reply = QMessageBox.question(
            self,
            "Claim Free Trial",
            f"Would you like to start your {self.TRIAL_DURATION_DAYS}-day free Pro trial?\n\n"
            "You'll get access to:\n"
            "• Faster download speeds\n"
            "• Priority support\n"
            "• Advanced video editing features\n"
            "• Batch processing\n"
            "• No ads\n\n"
            "No credit card required!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            # Calculate expiration date
            expires_at = QDateTime.currentDateTime().addDays(self.TRIAL_DURATION_DAYS)
            
            # Save to settings (local storage equivalent)
            self.settings.setValue('trial_claimed', True)
            self.settings.setValue('trial_expires_at', expires_at.toString(Qt.ISODate))
            self.settings.setValue('trial_claimed_at', QDateTime.currentDateTime().toString(Qt.ISODate))
            
            # Try to claim on server (if available)
            self.claim_trial_on_server()
            
            # Update UI
            self.update_trial_status()
            
            QMessageBox.information(
                self,
                "Trial Activated!",
                f"🎉 Your {self.TRIAL_DURATION_DAYS}-day free Pro trial is now active!\n\n"
                f"Trial expires on: {expires_at.toString('yyyy-MM-dd HH:mm')}\n\n"
                "Enjoy all Pro features!"
            )
    
    def claim_trial_on_server(self):
        """
        Attempt to claim trial on server (if API is available).
        This is a non-blocking operation that fails silently.
        """
        try:
            server_url = os.environ.get('UVDM_LICENSE_SERVER')
            if not server_url:
                # No server configured, skip
                return
            
            # Make API call to claim trial
            response = requests.post(
                f"{server_url}/api/claim-trial",
                json={
                    'duration_days': self.TRIAL_DURATION_DAYS
                },
                timeout=5
            )
            
            if response.status_code == 200:
                # Success - server has recorded the trial
                result = response.json()
                if result.get('success'):
                    # Optionally sync server expiration date
                    if 'expires_at' in result:
                        self.settings.setValue('trial_expires_at', result['expires_at'])
        except Exception:
            # Silently fail - local trial is still active
            pass


if __name__ == "__main__":
    # Test the widget
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    widget = TrialBannerWidget()
    widget.setWindowTitle("Trial Banner Test")
    widget.resize(600, 120)
    widget.show()
    sys.exit(app.exec_())
