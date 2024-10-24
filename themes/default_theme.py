# Updated stylesheet with rounded borders and larger font sizes
updated_stylesheet = """
/* General app styling */
QWidget {
    background-color: #2E2E2E; /* Dark grey background */
    color: #D3D3D3; /* Light grey text */
    font-family: Arial, sans-serif;
    font-size: 14px; /* Default font size */
}

/* Button styling */
QPushButton {
    background-color: #4D4D4D; /* Darker grey for button background */
    color: #FFFFFF; /* White text */
    border: 1px solid #3C3C3C;
    border-radius: 8px; /* More rounded borders */
    padding: 8px 12px; /* Increased padding for larger buttons */
    font-size: 14px; /* Larger font size for buttons */
}

QPushButton:hover {
    background-color: #666666; /* Lighter grey for hover */
}

QPushButton:pressed {
    background-color: #5E5E5E; /* Slightly lighter grey for pressed state */
}

/* Top bar buttons (Downloads, Batch Downloads, etc.) */
#topBarButton {
    background-color: #1B1B1B; /* Black for top bar */
    color: #F2A900; /* Yellow text */
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 14px;
}

#topBarButton:hover {
    background-color: #333333; /* Dark grey on hover */
}

/* Tab styling */
QTabBar::tab {
    background: #4D4D4D; /* Dark grey for tabs */
    color: #D3D3D3; /* Light grey text */
    padding: 10px;
    border: 1px solid #3C3C3C;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-size: 14px;
}

QTabBar::tab:selected {
    background: orange; /* Green for selected tab */
    color: #FFFFFF;
}

QTabBar::tab:hover {
    background: #666666; /* Lighter grey on hover */
}

/* Input fields */
QLineEdit, QComboBox {
    background-color: #3E3E3E; /* Darker grey for input background */
    color: #FFFFFF; /* White text */
    border: 1px solid #666666;
    border-radius: 5px; /* More rounded borders */
    padding: 6px;
    font-size: 14px;
}

QLineEdit:focus, QComboBox:focus {
    border: 1px solid #4CAF50; /* Green border when focused */
}

/* Checkbox styling */
QCheckBox {
    color: #D3D3D3; /* Light grey text */
    font-size: 14px;
}

/* Header styling */
QHeaderView::section {
    background-color: #4D4D4D; /* Dark grey background for headers */
    color: #D3D3D3; /* Light grey text */
    padding: 8px;
    border: 1px solid #3C3C3C;
    font-size: 14px;
}

/* Progress bar styling */
QProgressBar {
    background-color: #3C3C3C; /* Dark grey background */
    border: 1px solid #5E5E5E;
    border-radius: 8px;
    text-align: center;
    font-size: 14px;
}

QProgressBar::chunk {
    background-color: #4CAF50; /* Green progress indicator */
}

/* Scrollbar styling */
QScrollBar:vertical {
    background: #3C3C3C;
    width: 12px; /* Slightly wider for easier use */
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #5E5E5E;
    min-height: 20px;
    border-radius: 6px; /* Rounded scrollbar handle */
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
    padding: 6px;
    border-radius: 5px;
    font-size: 14px;
}
"""
