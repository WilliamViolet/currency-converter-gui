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

    def login(self, username: str, password: str) -> str:
        """Login to the currency service with the specified username and password.
        
        Args:
            username (str): The username for the account.
            password (str): The password for the account.

        Returns:
            str: A message indicating the success of the login.

        Raises:
            Exception: If the request to the currency service fails.
        """
        url = f"{self.base_url}/api/login"
        self._logger.info(f"Logging in with username: {username}")
        response = requests.post(url, json={"username": username, "password": password})
        
        if response.status_code == 200:
            self._logger.info("Login successful")
            return response.json()["access_token"]
        else:
            self._logger.error(f"Login failed: {response.status_code}")
            raise Exception(f"Login failed: {response.text}")
    
    def create_account(self, username: str, password: str) -> str:
        """Create an account with the specified username and password.
        
        Args:
            username (str): The username for the account.
            password (str): The password for the account.

        Returns:
            str: A message indicating the success of the account creation.

        Raises:
            Exception: If the request to the currency service fails.
        """
        url = f"{self.base_url}/api/create-account"
        self._logger.info(f"Creating account with username: {username}")
        response = requests.post(url, json={"username": username, "password": password})
        
        if response.status_code == 200:
            self._logger.info("Account created successfully")
            return response.json()["message"]
        else:
            self._logger.error(f"Failed to create account: {response.status_code}")
            raise Exception(f"Failed to create account: {response.text}")

    def get_supported_currencies(self, token: str) -> None: 
        """Get a list of supported currencies.
        
        Returns: 
            list: A list of supported currencies.

        Raises:
            Exception: If the request to the currency service fails.
        """
        self._logger.info("Token: %s", token)
        url = f"{self.base_url}/api/supported-currencies"
        headers = {"Authorization": f"Bearer {token}"}
        self._logger.info(f"Fetching supported currencies from currency service")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            self._logger.info("Successfully fetched supported currencies")
            return response.json()["message"]
        else:
            self._logger.error(f"Failed to fetch currencies: {response.status_code}")
            raise Exception(f"Failed to fetch currencies: {response.text}")

    def convert(self, base_currency: str, target_currency: str, amount: str, token: str) -> str:
        """Convert a file to the specified format.
        
        Args:
            base_currency (str): The base currency.
            target_currency (str): The target currency.
            amount (str): The amount to convert.
            token (str): The token for authentication.
        
        Returns:
            str: The converted amount.
        
        Raises:
            Exception: If the request to the currency service fails.
        """
        url = f"{self.base_url}/api/convert?base={base_currency}&to={target_currency}&amount={amount}"
        self._logger.info(f"Converting {amount} from {base_currency} to {target_currency}")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            self._logger.info("Conversion successful")
            return response.json()["message"]
        else:
            self._logger.error(f"Conversion failed: {response.status_code}")
            raise Exception(f"Conversion failed: {response.text}")