import sys
import os
from app.styles import apply_stylesheet
from themes.dark_theme import dark_theme_stylesheet
from themes.black_theme import black_theme_stylesheet
from themes.white_theme import white_theme_stylesheet
from themes.default_theme import updated_stylesheet

#work around for error in gridview mode. qt.gui.icc: fromIccProfile: failed minimal tag size sanity 
os.environ["QT_ENABLE_REGEXP_JIT"] = "0"

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
    # Example of applying a theme based on a setting
    app.setStyleSheet(updated_stylesheet)  # Switch to the appropriate theme
    #apply_stylesheet(app)
    window = YTDLPApp()
    # Apply the custom stylesheet
    window.show()
    sys.exit(app.exec_())
