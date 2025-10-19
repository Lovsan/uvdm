"""
Payment Widget - provides UI for Stripe and PayPal payment integration.
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QMessageBox, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
import requests
import os
import json


class PaymentWidget(QWidget):
    """Widget for payment integration (Stripe and PayPal)."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        main_layout = QVBoxLayout()
        
        # Title
        title = QLabel("Subscribe to Pro")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Plan info
        plan_group = QGroupBox("Pro Plan - $9.99/month")
        plan_layout = QVBoxLayout()
        
        features_text = """
<b>Pro Features Include:</b>
<ul>
    <li>🚀 Faster download speeds with priority servers</li>
    <li>📹 Advanced video editing and trimming</li>
    <li>🎬 Batch processing up to 100 videos</li>
    <li>☁️ Cloud storage integration</li>
    <li>🔄 Automatic format conversion</li>
    <li>📊 Detailed download analytics</li>
    <li>🎯 Ad-free experience</li>
    <li>💬 Priority customer support</li>
    <li>🔓 Access to exclusive features</li>
</ul>
        """
        
        features_label = QLabel(features_text)
        features_label.setWordWrap(True)
        plan_layout.addWidget(features_label)
        
        plan_group.setLayout(plan_layout)
        main_layout.addWidget(plan_group)
        
        # Payment methods
        payment_group = QGroupBox("Choose Payment Method")
        payment_layout = QVBoxLayout()
        
        # Stripe button
        stripe_layout = QHBoxLayout()
        stripe_icon = QLabel("💳")
        stripe_icon.setStyleSheet("font-size: 24px;")
        stripe_layout.addWidget(stripe_icon)
        
        self.stripe_button = QPushButton("Pay with Stripe")
        self.stripe_button.setStyleSheet("""
            QPushButton {
                background-color: #635BFF;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5247E6;
            }
            QPushButton:pressed {
                background-color: #4339CC;
            }
        """)
        self.stripe_button.clicked.connect(self.pay_with_stripe)
        stripe_layout.addWidget(self.stripe_button, 1)
        
        payment_layout.addLayout(stripe_layout)
        
        # PayPal button
        paypal_layout = QHBoxLayout()
        paypal_icon = QLabel("🅿️")
        paypal_icon.setStyleSheet("font-size: 24px;")
        paypal_layout.addWidget(paypal_icon)
        
        self.paypal_button = QPushButton("Pay with PayPal")
        self.paypal_button.setStyleSheet("""
            QPushButton {
                background-color: #0070BA;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005EA6;
            }
            QPushButton:pressed {
                background-color: #004C8C;
            }
        """)
        self.paypal_button.clicked.connect(self.pay_with_paypal)
        paypal_layout.addWidget(self.paypal_button, 1)
        
        payment_layout.addLayout(paypal_layout)
        
        # Info text
        info_label = QLabel(
            "💡 <i>Secure payment processing. Cancel anytime.</i>"
        )
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: #666; margin-top: 10px;")
        payment_layout.addWidget(info_label)
        
        payment_group.setLayout(payment_layout)
        main_layout.addWidget(payment_group)
        
        # Configuration status
        self.config_status_label = QLabel()
        self.config_status_label.setWordWrap(True)
        self.config_status_label.setStyleSheet("color: #888; font-size: 11px; font-style: italic;")
        main_layout.addWidget(self.config_status_label)
        
        self.update_config_status()
        
        main_layout.addStretch()
        self.setLayout(main_layout)
    
    def update_config_status(self):
        """Update the configuration status message."""
        config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'payments.example.json')
        
        if not os.path.exists(config_file):
            self.config_status_label.setText(
                "⚠️ Payment configuration not set up. See README for setup instructions."
            )
        else:
            self.config_status_label.setText(
                "ℹ️ Payment system is in placeholder mode. Configure API keys to enable real payments."
            )
    
    def pay_with_stripe(self):
        """Handle Stripe payment."""
        # Check if API is configured
        server_url = os.environ.get('UVDM_LICENSE_SERVER')
        if not server_url:
            self.show_configuration_message('Stripe')
            return
        
        try:
            # Call Stripe checkout endpoint
            response = requests.post(
                f"{server_url}/api/create-checkout-session",
                json={
                    'plan': 'pro_monthly',
                    'success_url': 'uvdm://payment/success',
                    'cancel_url': 'uvdm://payment/cancel'
                },
                timeout=5
            )
            
            if response.status_code == 501:
                # Not implemented
                self.show_configuration_message('Stripe')
            elif response.status_code == 200:
                result = response.json()
                checkout_url = result.get('checkout_url')
                if checkout_url:
                    # Open checkout URL in browser
                    import webbrowser
                    webbrowser.open(checkout_url)
                else:
                    QMessageBox.warning(self, "Error", "Invalid response from payment server.")
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Payment server error: {response.status_code}"
                )
        except requests.exceptions.Timeout:
            QMessageBox.warning(
                self,
                "Timeout",
                "Payment server is not responding. Please try again later."
            )
        except Exception as e:
            self.show_configuration_message('Stripe')
    
    def pay_with_paypal(self):
        """Handle PayPal payment."""
        # Check if API is configured
        server_url = os.environ.get('UVDM_LICENSE_SERVER')
        if not server_url:
            self.show_configuration_message('PayPal')
            return
        
        try:
            # Call PayPal order endpoint
            response = requests.post(
                f"{server_url}/api/paypal/create-order",
                json={
                    'plan': 'pro_monthly',
                    'return_url': 'uvdm://payment/success',
                    'cancel_url': 'uvdm://payment/cancel'
                },
                timeout=5
            )
            
            if response.status_code == 501:
                # Not implemented
                self.show_configuration_message('PayPal')
            elif response.status_code == 200:
                result = response.json()
                approval_url = result.get('approval_url')
                if approval_url:
                    # Open approval URL in browser
                    import webbrowser
                    webbrowser.open(approval_url)
                else:
                    QMessageBox.warning(self, "Error", "Invalid response from payment server.")
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Payment server error: {response.status_code}"
                )
        except requests.exceptions.Timeout:
            QMessageBox.warning(
                self,
                "Timeout",
                "Payment server is not responding. Please try again later."
            )
        except Exception as e:
            self.show_configuration_message('PayPal')
    
    def show_configuration_message(self, provider):
        """Show configuration instructions."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(f"{provider} Configuration Required")
        msg.setText(f"<h3>{provider} payment integration is not yet configured.</h3>")
        
        instructions = f"""
<p>To enable {provider} payments, the administrator needs to:</p>

<ol>
    <li>Configure {provider} API keys in <code>config/payments.json</code></li>
    <li>Set environment variables:
        <ul>
            <li><code>STRIPE_PUBLISHABLE_KEY</code></li>
            <li><code>STRIPE_SECRET_KEY</code></li>
        </ul>
    </li>
    <li>Restart the API server</li>
</ol>

<p>See <code>config/payments.example.json</code> and README.md for detailed setup instructions.</p>

<p><b>For now, this is a placeholder implementation.</b></p>
        """
        
        if provider == 'PayPal':
            instructions = f"""
<p>To enable {provider} payments, the administrator needs to:</p>

<ol>
    <li>Configure {provider} API keys in <code>config/payments.json</code></li>
    <li>Set environment variables:
        <ul>
            <li><code>PAYPAL_CLIENT_ID</code></li>
            <li><code>PAYPAL_SECRET</code></li>
        </ul>
    </li>
    <li>Restart the API server</li>
</ol>

<p>See <code>config/payments.example.json</code> and README.md for detailed setup instructions.</p>

<p><b>For now, this is a placeholder implementation.</b></p>
            """
        
        msg.setInformativeText(instructions)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


if __name__ == "__main__":
    # Test the widget
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    widget = PaymentWidget()
    widget.setWindowTitle("Payment Widget Test")
    widget.resize(500, 600)
    widget.show()
    sys.exit(app.exec_())
