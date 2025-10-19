"""
License manager dialog for UVDM application.
Provides UI for managing and verifying licenses.
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTextEdit, QGroupBox, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from app.license_client import LicenseClient
import traceback


class LicenseVerifyWorker(QThread):
    """Worker thread for license verification."""
    
    result_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, client, license_key, action='verify'):
        super().__init__()
        self.client = client
        self.license_key = license_key
        self.action = action
    
    def run(self):
        """Run license verification in background."""
        try:
            if self.action == 'verify':
                result = self.client.verify_license(self.license_key)
            elif self.action == 'activate':
                result = self.client.activate_license(self.license_key)
            elif self.action == 'deactivate':
                result = self.client.deactivate_license(self.license_key)
            else:
                result = {'error': 'Unknown action'}
            
            self.result_ready.emit(result)
        except Exception as e:
            self.error_occurred.emit(f"Error: {str(e)}\n{traceback.format_exc()}")


class LicenseDialog(QDialog):
    """Dialog for managing licenses."""
    
    def __init__(self, parent=None, server_url=None):
        super().__init__(parent)
        self.setWindowTitle("UVDM License Manager")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        
        # Initialize license client
        self.client = LicenseClient(server_url=server_url)
        self.worker = None
        
        self.setup_ui()
        self.check_existing_license()
    
    def setup_ui(self):
        """Setup the UI components."""
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("License Management")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Server status
        self.status_label = QLabel()
        self.update_server_status()
        layout.addWidget(self.status_label)
        
        # License key input group
        license_group = QGroupBox("License Key")
        license_layout = QVBoxLayout()
        
        # License key input
        key_input_layout = QHBoxLayout()
        self.license_key_input = QLineEdit()
        self.license_key_input.setPlaceholderText("Enter your license key (e.g., UVDM-XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX)")
        key_input_layout.addWidget(self.license_key_input)
        
        license_layout.addLayout(key_input_layout)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.verify_button = QPushButton("Verify License")
        self.verify_button.clicked.connect(self.verify_license)
        button_layout.addWidget(self.verify_button)
        
        self.activate_button = QPushButton("Activate License")
        self.activate_button.clicked.connect(self.activate_license)
        button_layout.addWidget(self.activate_button)
        
        self.deactivate_button = QPushButton("Deactivate License")
        self.deactivate_button.clicked.connect(self.deactivate_license)
        button_layout.addWidget(self.deactivate_button)
        
        license_layout.addLayout(button_layout)
        license_group.setLayout(license_layout)
        layout.addWidget(license_group)
        
        # Status/Result display
        result_group = QGroupBox("License Status")
        result_layout = QVBoxLayout()
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMaximumHeight(200)
        result_layout.addWidget(self.result_text)
        
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)
        
        # Machine ID display
        machine_group = QGroupBox("Machine Information")
        machine_layout = QVBoxLayout()
        
        machine_id_label = QLabel(f"Machine ID: {self.client.machine_id}")
        machine_id_label.setWordWrap(True)
        machine_id_label.setStyleSheet("font-family: monospace;")
        machine_layout.addWidget(machine_id_label)
        
        machine_group.setLayout(machine_layout)
        layout.addWidget(machine_group)
        
        # Close button
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        close_layout.addWidget(close_button)
        
        layout.addLayout(close_layout)
        
        self.setLayout(layout)
    
    def update_server_status(self):
        """Update the server status label."""
        if self.client.check_server_status():
            self.status_label.setText("✓ License server is online")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.status_label.setText("✗ License server is offline (offline mode available)")
            self.status_label.setStyleSheet("color: orange; font-weight: bold;")
    
    def check_existing_license(self):
        """Check if there's a cached license."""
        cache = self.client._load_cache()
        if cache.get('license_key'):
            self.license_key_input.setText(cache['license_key'])
            self.result_text.append("Found cached license key.")
            self.verify_license()
    
    def verify_license(self):
        """Verify the entered license key."""
        license_key = self.license_key_input.text().strip()
        
        if not license_key:
            QMessageBox.warning(self, "Input Error", "Please enter a license key.")
            return
        
        self.set_buttons_enabled(False)
        self.result_text.append(f"\nVerifying license: {license_key}...")
        
        self.worker = LicenseVerifyWorker(self.client, license_key, 'verify')
        self.worker.result_ready.connect(self.on_verify_result)
        self.worker.error_occurred.connect(self.on_error)
        self.worker.start()
    
    def activate_license(self):
        """Activate the entered license key."""
        license_key = self.license_key_input.text().strip()
        
        if not license_key:
            QMessageBox.warning(self, "Input Error", "Please enter a license key.")
            return
        
        self.set_buttons_enabled(False)
        self.result_text.append(f"\nActivating license: {license_key}...")
        
        self.worker = LicenseVerifyWorker(self.client, license_key, 'activate')
        self.worker.result_ready.connect(self.on_activate_result)
        self.worker.error_occurred.connect(self.on_error)
        self.worker.start()
    
    def deactivate_license(self):
        """Deactivate the entered license key."""
        license_key = self.license_key_input.text().strip()
        
        if not license_key:
            QMessageBox.warning(self, "Input Error", "Please enter a license key.")
            return
        
        reply = QMessageBox.question(
            self, 
            "Confirm Deactivation",
            "Are you sure you want to deactivate this license?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.set_buttons_enabled(False)
            self.result_text.append(f"\nDeactivating license: {license_key}...")
            
            self.worker = LicenseVerifyWorker(self.client, license_key, 'deactivate')
            self.worker.result_ready.connect(self.on_deactivate_result)
            self.worker.error_occurred.connect(self.on_error)
            self.worker.start()
    
    def on_verify_result(self, result):
        """Handle verification result."""
        self.set_buttons_enabled(True)
        
        if result.get('valid'):
            self.result_text.append("✓ License is VALID!")
            self.result_text.append(f"  License Type: {result.get('license_type', 'N/A')}")
            
            expiry = result.get('expiry_date')
            if expiry:
                self.result_text.append(f"  Expiry Date: {expiry}")
            else:
                self.result_text.append("  Expiry Date: Never")
            
            features = result.get('features', [])
            if features:
                self.result_text.append(f"  Features: {', '.join(features)}")
            
            if result.get('offline'):
                cache_age = result.get('cache_age_days', 0)
                self.result_text.append(f"  Mode: Offline (cache age: {cache_age} days)")
            else:
                self.result_text.append("  Mode: Online")
        else:
            error = result.get('error', 'Unknown error')
            self.result_text.append(f"✗ License verification failed: {error}")
            
            if result.get('offline'):
                self.result_text.append("  Note: Server is offline, using cached data")
    
    def on_activate_result(self, result):
        """Handle activation result."""
        self.set_buttons_enabled(True)
        
        if result.get('success'):
            self.result_text.append("✓ License activated successfully!")
            self.result_text.append(f"  {result.get('message', '')}")
            
            # Automatically verify after successful activation
            self.verify_license()
        else:
            error = result.get('error', 'Unknown error')
            self.result_text.append(f"✗ License activation failed: {error}")
    
    def on_deactivate_result(self, result):
        """Handle deactivation result."""
        self.set_buttons_enabled(True)
        
        if result.get('success'):
            self.result_text.append("✓ License deactivated successfully!")
            self.result_text.append(f"  {result.get('message', '')}")
        else:
            error = result.get('error', 'Unknown error')
            self.result_text.append(f"✗ License deactivation failed: {error}")
    
    def on_error(self, error_message):
        """Handle errors."""
        self.set_buttons_enabled(True)
        self.result_text.append(f"\n✗ Error occurred: {error_message}")
    
    def set_buttons_enabled(self, enabled):
        """Enable or disable action buttons."""
        self.verify_button.setEnabled(enabled)
        self.activate_button.setEnabled(enabled)
        self.deactivate_button.setEnabled(enabled)


def show_license_dialog(parent=None, server_url=None):
    """
    Show the license dialog.
    
    Args:
        parent: Parent widget
        server_url: Optional server URL
        
    Returns:
        Dialog result (accepted or rejected)
    """
    dialog = LicenseDialog(parent, server_url)
    return dialog.exec_()
