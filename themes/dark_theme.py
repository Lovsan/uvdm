dark_theme_stylesheet = """
/* General app styling */
QWidget {
    background-color: #2E2E2E; /* Dark grey background */
    color: #D3D3D3; /* Light grey text */
    font-family: Arial, sans-serif;
    font-size: 14px;
}

/* Button styling */
QPushButton {
    background-color: #4D4D4D;
    color: #FFFFFF;
    border: 1px solid #3C3C3C;
    border-radius: 5px;
    padding: 5px 10px;
}

QPushButton:hover {
    background-color: #5E5E5E;
}

QPushButton:pressed {
    background-color: #707070;
}

/* Top bar buttons */
#topBarButton {
    background-color: #1B1B1B;
    color: #F2A900;
}

/* Tab styling */
QTabBar::tab {
    background: #4D4D4D;
    color: #D3D3D3;
}

QTabBar::tab:selected {
    background: #4CAF50;
    color: #FFFFFF;
}

/* Input fields */
QLineEdit, QComboBox {
    background-color: #3C3C3C;
    color: #FFFFFF;
}

/* Checkbox styling */
QCheckBox {
    color: #D3D3D3;
}

/* Header styling */
QHeaderView::section {
    background-color: #4D4D4D;
    color: #D3D3D3;
}

/* Progress bar styling */
QProgressBar {
    background-color: #3C3C3C;
}

QProgressBar::chunk {
    background-color: #4CAF50;
}

/* Scrollbar styling */
QScrollBar:vertical {
    background: #3C3C3C;
}

QScrollBar::handle:vertical {
    background: #5E5E5E;
}

/* Tooltips */
QToolTip {
    background-color: #4D4D4D;
    color: #FFFFFF;
}
"""
