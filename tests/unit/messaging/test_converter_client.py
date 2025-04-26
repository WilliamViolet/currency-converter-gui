import unittest
from unittest.mock import MagicMock, patch
from converter_gui.messaging.converter_client import ConverterClient

class TestConverterClient(unittest.TestCase):
    def setUp(self):
        """Set up the ConverterClient instance for testing."""
        self.client = ConverterClient("http://mock_host:mock_port")

    @patch("converter_gui.messaging.converter_client.requests.get")
    def test_get_supported_currencies_success(self, mock_get):
        """Test getting supported currencies successfully."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": ["USD", "EUR"]}
        mock_get.return_value = mock_response

        result = self.client.get_supported_currencies()

        self.assertEqual(result, ["USD", "EUR"])
        mock_get.assert_called_once_with("http://mock_host:mock_port/api/supported-currencies")
    
    @patch("converter_gui.messaging.converter_client.requests.get")
    def test_get_supported_currencies_failure(self, mock_get):
        """Test getting supported currencies with a failure."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.client.get_supported_currencies()

        self.assertEqual(str(context.exception), "Failed to fetch currencies: Internal Server Error")
        mock_get.assert_called_once_with("http://mock_host:mock_port/api/supported-currencies")
    
    @patch("converter_gui.messaging.converter_client.requests.get")
    def test_convert_success(self, mock_get):
        """Test converting currencies successfully."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "10.00"}
        mock_get.return_value = mock_response

        result = self.client.convert("USD", "EUR", "5.00")

        self.assertEqual(result, "10.00")
        mock_get.assert_called_once_with("http://mock_host:mock_port/api/convert?base=USD&to=EUR&amount=5.00")
    
    @patch("converter_gui.messaging.converter_client.requests.get")
    def test_convert_failure(self, mock_get):
        """Test converting currencies with a failure."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.client.convert("USD", "EUR", "5.00")

        self.assertEqual(str(context.exception), "Conversion failed: Internal Server Error")
        mock_get.assert_called_once_with("http://mock_host:mock_port/api/convert?base=USD&to=EUR&amount=5.00")