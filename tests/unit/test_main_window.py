import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from converter_gui.main_window import MainWindow

class TestMainWindow(unittest.TestCase):
    @patch("converter_gui.messaging.converter_client.ConverterClient.get_supported_currencies")
    @patch("converter_gui.config.Config.get")
    def setUp(self, mock_config, mock_client):
        mock_client.return_value = MagicMock()
        mock_config.return_value = ""
        self.main_window = MainWindow()

    def test_convert_successful(self):
        client = MagicMock()
        client.convert.return_value = "10.00"
        self.main_window.result = MagicMock()

        self.main_window.convert(client, "USD", "EUR", "5.00")

        client.convert.assert_called_with("USD", "EUR", "5.00")
        self.main_window.result.setText.assert_called_with("10.00")

    # def test_convert_exception(self):
    #     client = MagicMock()
    #     client.convert.side_effect = Exception("Conversion failed")
    #     self.main_window._logger = MagicMock()
    #     self.main_window.result = MagicMock()

    #     self.main_window.convert(client, "USD", "EUR", "5.00")

    #     client.convert.assert_called_with("USD", "EUR", "5.00")
    #     self.main_window._logger.error.assert_called_with("Failed to convert: Conversion failed")
    #     self.main_window.result.setText.assert_not_called()

