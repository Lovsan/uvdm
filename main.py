import sys
import os

# Ensure data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Ensure thumbnails directory exists
if not os.path.exists(os.path.join('data', 'thumbnails')):
    os.makedirs(os.path.join('data', 'thumbnails'))

from PyQt5.QtWidgets import QApplication
from app.main_window import YTDLPApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YTDLPApp()
    window.show()
    sys.exit(app.exec_())
