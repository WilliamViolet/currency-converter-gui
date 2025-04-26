import unittest
from unittest.mock import patch, mock_open
from configparser import ConfigParser
from converter_gui.config import Config

class TestConfig(unittest.TestCase):
    def setUp(self):
        """Set up the Config instance for testing."""
        self.config = Config()

    @patch("builtins.open", new_callable=mock_open, read_data="[section1]\nkey=value\n")
    def test_load_config_success(self, mock_file):
        """Test loading a valid configuration file."""
        self.config._load_config("mock_config.ini")
        self.assertTrue(self.config.has_section("section1"))
        self.assertEqual(self.config.config.get("section1", "key"), "value")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_config_file_not_found(self, mock_file):
        """Test loading a non-existent configuration file."""
        with self.assertRaises(FileNotFoundError):
            self.config._load_config("non_existent_config.ini")

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_load_config_empty_file(self, mock_file):
        """Test loading an empty configuration file."""
        with self.assertRaises(FileNotFoundError):
            self.config._load_config("empty_config.ini")

    @patch("builtins.open", new_callable=mock_open, read_data="[section1]\nkey=value\n")
    def test_has_section(self, mock_file):
        """Test the has_section method."""
        self.config._load_config("mock_config.ini")
        self.assertTrue(self.config.has_section("section1"))
        self.assertFalse(self.config.has_section("non_existent_section"))
    
    @patch("builtins.open", new_callable=mock_open, read_data="[section1]\nkey=value\n")
    def test_get__no_option_error(self, mock_file):
        """Test the get method with a non-existent option."""
        self.config._load_config("mock_config.ini")
        with self.assertRaises(ValueError):
            self.config.get("section1", "non_existent_key")
    
    @patch("builtins.open", new_callable=mock_open, read_data="[section1]\nkey=value\n")
    def test_get__no_section_error(self, mock_file):
        """Test the get method with a non-existent section."""
        self.config._load_config("mock_config.ini")
        with self.assertRaises(ValueError):
            self.config.get("non_existent_section", "key")

    @patch("builtins.open", new_callable=mock_open, read_data="[section1]\nkey=value\n")
    def test_get(self, mock_file):
        """Test the get method with a valid section and option."""
        self.config._load_config("mock_config.ini")
        self.assertEqual(self.config.get("section1", "key"), "value")
