
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

class ClickableLabel(QLabel):
    """A label that emits a signal when clicked."""
    def mousePressEvent(self, event):
        self.clicked.emit()

def create_button(text, parent=None):
    """Utility function to create a QPushButton."""
    button = QPushButton(text, parent)
    return button

def create_vertical_layout(widget_list):
    """Creates a QVBoxLayout with the provided list of widgets."""
    layout = QVBoxLayout()
    for widget in widget_list:
        layout.addWidget(widget)
    return layout
