white_theme_stylesheet = """
/* General app styling */
QWidget {
    background-color: #F0F0F0; /* Light grey background */
    color: #2E2E2E; /* Dark grey text */
}

/* Button styling */
QPushButton {
    background-color: #E0E0E0;
    color: #2E2E2E;
    border: 1px solid #BEBEBE;
}

QPushButton:hover {
    background-color: #D8D8D8;
}

/* Top bar buttons */
#topBarButton {
    background-color: #E0E0E0;
    color: #333333;
}

/* Tab styling */
QTabBar::tab {
    background: #E0E0E0;
    color: #2E2E2E;
}

QTabBar::tab:selected {
    background: #BEBEBE;
    color: #2E2E2E;
}

/* Input fields */
QLineEdit, QComboBox {
    background-color: #FFFFFF;
    color: #2E2E2E;
}

/* Checkbox styling */
QCheckBox {
    color: #2E2E2E;
}

/* Header styling */
QHeaderView::section {
    background-color: #D0D0D0;
    color: #2E2E2E;
}

/* Progress bar styling */
QProgressBar {
    background-color: #E0E0E0;
}

QProgressBar::chunk {
    background-color: #4CAF50;
}

/* Scrollbar styling */
QScrollBar:vertical {
    background: #E0E0E0;
}

QScrollBar::handle:vertical {
    background: #C0C0C0;
}

/* Tooltips */
QToolTip {
    background-color: #E0E0E0;
    color: #2E2E2E;
}
"""
