import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt

class LogsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # Label for download logs
        self.download_logs_label = QLabel("Download Logs:")
        self.layout.addWidget(self.download_logs_label)

        # Text area for download logs
        self.download_logs_text = QTextEdit()
        self.download_logs_text.setReadOnly(True)
        self.download_logs_text.setPlainText(self.load_logs('logs.log'))
        self.layout.addWidget(self.download_logs_text)

        # Label for error logs
        self.error_logs_label = QLabel("Error Logs:")
        self.layout.addWidget(self.error_logs_label)

        # Text area for error logs
        self.error_logs_text = QTextEdit()
        self.error_logs_text.setReadOnly(True)
        self.error_logs_text.setPlainText(self.load_logs('error_logs.log'))
        self.layout.addWidget(self.error_logs_text)

        # Clear logs button
        self.clear_logs_button = QPushButton("Clear Logs")
        self.clear_logs_button.clicked.connect(self.clear_logs)
        self.layout.addWidget(self.clear_logs_button)

        self.setLayout(self.layout)

    def load_logs(self, log_file):
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    return f.read()
            except UnicodeDecodeError:
                # Handle decoding errors by reading with 'replace' error handling
                with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
                    return f.read()
        else:
            return f"{log_file} not found."

    def clear_logs(self):
        open('logs.log', 'w', encoding='utf-8').close()
        open('error_logs.log', 'w', encoding='utf-8').close()
        self.download_logs_text.clear()
        self.error_logs_text.clear()
