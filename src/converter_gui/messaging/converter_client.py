import requests
import logging

class ConverterClient:
    """A client for the converter service."""
    def __init__(self, base_url) -> None:
        """Initialize the client with the base URL of the converter service.
        
        Args:
            base_url (str): The base URL of the converter service.
        """
        self.base_url = base_url
        self._logger = logging.getLogger(__name__)

    def get_supported_currencies(self) -> None: 
        """Get a list of supported currencies.
        
        Returns: 
            list: A list of supported currencies.

        Raises:
            Exception: If the request to the currency service fails.
        """
        url = f"{self.base_url}/api/supported-currencies"
        self._logger.info(f"Fetching supported currencies from currency service")
        response = requests.get(url)
        
        if response.status_code == 200:
            self._logger.info("Successfully fetched supported currencies")
            return response.json()["message"]
        else:
            self._logger.error(f"Failed to fetch currencies: {response.status_code}")
            raise Exception(f"Failed to fetch currencies: {response.text}")

    def convert(self, base_currency: str, target_currency: str, amount: str) -> str:
        """Convert a file to the specified format.
        
        Args:
            base_currency (str): The base currency.
            target_currency (str): The target currency.
            amount (str): The amount to convert.
        
        Returns:
            str: The converted amount.
        
        Raises:
            Exception: If the request to the currency service fails.
        """
        url = f"{self.base_url}/api/convert?base={base_currency}&to={target_currency}&amount={amount}"
        self._logger.info(f"Converting {amount} from {base_currency} to {target_currency}")
        response = requests.get(url)
        
        if response.status_code == 200:
            self._logger.info("Conversion successful")
            return response.json()["message"]
        else:
            self._logger.error(f"Conversion failed: {response.status_code}")
            raise Exception(f"Conversion failed: {response.text}")