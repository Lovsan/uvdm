
# Complete stylesheet for the app

stylesheet = """
/* General app styling */
QWidget {
    background-color: #2E2E2E; /* Dark grey background */
    color: #D3D3D3; /* Light grey text */
    font-family: Arial, sans-serif;
    font-size: 14px;
}

/* Button styling */
QPushButton {
    background-color: #4D4D4D; /* Darker grey for button background */
    color: #FFFFFF; /* White text */
    border: 1px solid #3C3C3C;
    border-radius: 5px;
    padding: 5px 10px;
}

QPushButton:hover {
    background-color: #5E5E5E; /* Slightly lighter grey for hover */
}

QPushButton:pressed {
    background-color: #707070; /* Even lighter grey for active state */
}

/* Top bar buttons (Downloads, Batch Downloads, etc.) */
#topBarButton {
    background-color: #1B1B1B; /* Black for top bar */
    color: #F2A900; /* Yellow text */
    border: none;
    padding: 8px 15px;
}

#topBarButton:hover {
    background-color: #333333; /* Dark grey on hover */
}

/* Tab styling */
QTabBar::tab {
    background: #4D4D4D; /* Dark grey for tabs */
    color: #D3D3D3; /* Light grey text */
    padding: 8px;
    border: 1px solid #3C3C3C;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}

QTabBar::tab:selected {
    background: #4CAF50; /* Green for selected tab */
    color: #FFFFFF;
}

QTabBar::tab:hover {
    background: #5E5E5E; /* Slightly lighter grey on hover */
}

/* Input fields */
QLineEdit, QComboBox {
    background-color: #3C3C3C; /* Dark grey input background */
    color: #FFFFFF; /* White text */
    border: 1px solid #5E5E5E;
    border-radius: 3px;
    padding: 5px;
}

QLineEdit:focus, QComboBox:focus {
    border: 1px solid #4CAF50; /* Green border when focused */
}

/* Checkbox styling */
QCheckBox {
    color: #D3D3D3; /* Light grey text */
}

/* Progress bar styling */
QProgressBar {
    background-color: #3C3C3C; /* Dark grey background */
    border: 1px solid #5E5E5E;
    border-radius: 5px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #4CAF50; /* Green progress indicator */
}

/* Scrollbar styling */
QScrollBar:vertical {
    background: #3C3C3C;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #5E5E5E;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #707070;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    background: none;
}

/* Tooltips */
QToolTip {
    background-color: #4D4D4D;
    color: #FFFFFF;
    border: 1px solid #707070;
    padding: 5px;
    border-radius: 3px;
}
"""

# Function to apply the stylesheet
def apply_stylesheet(app):
    app.setStyleSheet(stylesheet)
