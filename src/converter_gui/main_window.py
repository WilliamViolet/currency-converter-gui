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
        host = config.get("converter_service", "host")
        port = config.get("converter_service", "port")
        self.client = ConverterClient(f"http://{host}:{port}")
        self.token = None


    def create_create_acount_ui(self):
        """Create the login window for the currency converter."""
        self.login_window = QWidget()
        self.login_window.setWindowTitle("Login")
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Welcome to the Currency Converter!"))
        layout.addWidget(QLabel("Please enter your username and password."))
        
        username_layout = QHBoxLayout()
        password_layout = QHBoxLayout()

        username_label = QLabel("Username:")
        self.username_input = QLineEdit("Username")

        password_label = QLabel("Password:")
        self.password_input = QLineEdit("Password")

        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        login_button = QPushButton("Login")
        login_button.clicked.connect(lambda: self.login())

        create_account_button = QPushButton("Create Account")
        create_account_button.clicked.connect(lambda: self.create_account())

        layout.addLayout(username_layout)
        layout.addLayout(password_layout)
        layout.addWidget(login_button)
        layout.addWidget(create_account_button)

        self.login_window.setLayout(layout)
        self.login_window.show()
        sys.exit(self.app.exec_())

    def login(self): 
        """Handle the login process."""
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            self.token = self.client.login(username, password)
            self._logger.info(f"Login successful for user: {username}")
            QMessageBox.information(self.login_window, "Success", "Login successful!")
            self.login_window.close()
            self._create_ui()
        except Exception as e:
            self._logger.error(f"Login failed: {e}")
            QMessageBox.critical(self.login_window, "Error", f"Login failed: {e}")

    def create_account(self): 
        """Handle the login process."""
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            self.client.create_account(username, password)
            self._logger.info(f"Login successful for user: {username}")
            QMessageBox.information(self.login_window, "Success", "Login successful!")
            self.login_window.close()
        except Exception as e:
            self._logger.error(f"Login failed: {e}")
            QMessageBox.critical(self.login_window, "Error", f"Login failed: {e}")

    def _create_ui(self): 
        """Create the user interface for the currency converter."""
        self.window.setWindowTitle("Currency Converter")
        # window.setGeometry(700, 700, 700, 700)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to the Currency Converter!"))

        # try:
        supported_currencies = self.client.get_supported_currencies(self.token)
        # except Exception:
        #     self._logger.error("Failed to fetch supported currencies")
        #     QMessageBox.critical(self.window, "Error", "Failed to fetch supported currencies.")
        #     sys.exit(1)
        
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
        convert_button.clicked.connect(lambda: self.convert(self.client, from_combo.currentText(), to_combo.currentText(), input_layout.itemAt(1).widget().text(), self.token))

        layout.addLayout(to_layout)
        layout.addLayout(from_layout)
        layout.addLayout(result_layout)
        layout.addWidget(convert_button)

        self.window.setLayout(layout)
        self.window.show()
    
    def start(self): 
        self.window.show()
        sys.exit(self.app.exec_())

    def convert(self, client: ConverterClient, from_currency: str, to_currency: str, amount: str, token: str) -> str:
        """Convert the amount from one currency to another.
        
        Args:
            client (ConverterClient): The client for the converter service.
            from_currency (str): The currency to convert from.
            to_currency (str): The currency to convert to.
            amount (str): The amount to convert.
            token (str): The token for authentication.
        
        Returns: 
            str: The converted amount.
        
        Raises:
            Exception: If the conversion fails.
        """
        try:
            result = client.convert(from_currency, to_currency, amount, token)
            self._logger.debug(f"Converted {amount} {from_currency} to {to_currency}: {result}")
            self.result.setText(result)
        except Exception as e:
            self._logger.error(f"Failed to convert: {e}")
            QMessageBox.critical(self.window, "Error", f"Failed to convert: {e}")