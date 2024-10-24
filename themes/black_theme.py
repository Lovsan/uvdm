black_theme_stylesheet = """
/* General app styling */
QWidget {
    background-color: #1B1B1B; /* Black background */
    color: #F2F2F2; /* Bright grey text */
}

/* Button styling */
QPushButton {
    background-color: #333333;
    color: #F2F2F2;
    border: 1px solid #4D4D4D;
}

QPushButton:hover {
    background-color: #4D4D4D;
}

/* Top bar buttons */
#topBarButton {
    background-color: #000000;
    color: #F2A900;
}

/* Tab styling */
QTabBar::tab {
    background: #333333;
    color: #F2F2F2;
}

QTabBar::tab:selected {
    background: #F2A900;
    color: #000000;
}

/* Input fields */
QLineEdit, QComboBox {
    background-color: #262626;
    color: #F2F2F2;
}

/* Checkbox styling */
QCheckBox {
    color: #F2F2F2;
}

/* Header styling */
QHeaderView::section {
    background-color: #333333;
    color: #F2F2F2;
}

/* Progress bar styling */
QProgressBar {
    background-color: #262626;
}

QProgressBar::chunk {
    background-color: #F2A900;
}

/* Scrollbar styling */
QScrollBar:vertical {
    background: #262626;
}

QScrollBar::handle:vertical {
    background: #4D4D4D;
}

/* Tooltips */
QToolTip {
    background-color: #333333;
    color: #F2F2F2;
}
"""
