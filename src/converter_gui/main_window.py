import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QLineEdit, QPushButton
import logging
from converter_gui.messaging.converter_client import ConverterClient
from converter_gui.config import config

class MainWindow():
    """Main window for the currency converter application."""
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self._create_ui()

    def _create_ui(self): 
        """Create the user interface for the currency converter."""
        host = config.get("converter_service", "host")
        port = config.get("converter_service", "port")

        client = ConverterClient(f"http://{host}:{port}")
        self.window.setWindowTitle("Currency Converter")
        # window.setGeometry(700, 700, 700, 700)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to the Currency Converter!"))

        try:
            supported_currencies = client.get_supported_currencies()["message"]
        except Exception:
            self._logger.error("Failed to fetch supported currencies")
            QMessageBox.critical(self.window, "Error", "Failed to fetch supported currencies.")
            sys.exit(1)
        
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Amount:"))
        input_layout.addWidget(QLineEdit("0.00"))
        layout.addLayout(input_layout)


        to_combo = QComboBox()
        to_combo.addItems(supported_currencies)
        to_layout = QHBoxLayout()
        to_layout.addWidget(QLabel("To:"))
        to_layout.addWidget(to_combo)

        from_combo = QComboBox()
        from_combo.addItems(["USD"])
        from_layout = QHBoxLayout()
        from_layout.addWidget(QLabel("From:"))
        from_layout.addWidget(from_combo)

        self.result = QLabel()
        result_layout = QHBoxLayout()
        result_layout.addWidget(QLabel("Result:"))
        result_layout.addWidget(self.result)

        convert_button = QPushButton("Convert")
        convert_button.clicked.connect(lambda: self.convert(client, from_combo.currentText(), to_combo.currentText(), input_layout.itemAt(1).widget().text()))

        layout.addLayout(to_layout)
        layout.addLayout(from_layout)
        layout.addLayout(result_layout)
        layout.addWidget(convert_button)

        self.window.setLayout(layout)
    
    def start(self): 
        self.window.show()
        sys.exit(self.app.exec_())

    def convert(self, client: ConverterClient, from_currency: str, to_currency: str, amount: str):
        """Convert the amount from one currency to another.
        
        Args:
            client (ConverterClient): The client for the converter service.
            from_currency (str): The currency to convert from.
            to_currency (str): The currency to convert to.
            amount (str): The amount to convert.
        
        Returns: 
            str: The converted amount.
        
        Raises:
            Exception: If the conversion fails.
        """
        try:
            result = client.convert(from_currency, to_currency, amount)
            self._logger.debug(f"Converted {amount} {from_currency} to {to_currency}: {result}")
            self.result.setText(result)
        except Exception as e:
            self._logger.error(f"Failed to convert: {e}")
            QMessageBox.critical(None, "Error", f"Failed to convert: {e}")