import logging
from PyQt5.QtCore import pyqtSignal, QObject

# Configure logging for the main log file
logging.basicConfig(
    filename='logs.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s',
    encoding='utf-8'  # Specify UTF-8 encoding
)

error_logger = logging.getLogger('error_logger')
error_handler = logging.FileHandler('error_logs.log', mode='a', encoding='utf-8')  # Specify UTF-8 encoding
error_handler.setLevel(logging.ERROR)
error_logger.addHandler(error_handler)

class YTDLPLogger(QObject):
    output_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def debug(self, msg):
        logging.debug(msg)
        self.output_signal.emit(msg)

    def info(self, msg):
        logging.info(msg)
        self.output_signal.emit(msg)

    def warning(self, msg):
        logging.warning(msg)
        self.output_signal.emit(f"WARNING: {msg}")

    def error(self, msg):
        logging.error(msg)
        error_logger.error(msg)
        self.output_signal.emit(f"ERROR: {msg}")
