import configparser

class Config: 
    """Configuration handler for the application."""
    def __init__(self) -> None:
        """Initialize the Config class."""
        self.config = configparser.ConfigParser()
    
    def _load_config(self, config_file: str) -> None:
        """Load configuration from the specified file.
        
        Args:
            config_file (str): Path to the configuration file.
        
        Raises:
            FileNotFoundError: If the configuration file is not found.
            Exception: If there is an error loading the configuration.
        """
        try:
            self.config.read(config_file)
            if not self.config.sections():
                raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
        except Exception as e:
            print(f"Error loading configuration: {e}")
            raise
    
    def has_section(self, section: str) -> bool:
        """Check if a section exists in the configuration.
        
        Args:
            section (str): The section to check.
        
        Returns:
            bool: True if the section exists, False otherwise.
        """
        return self.config.has_section(section)
    
    def get(self, section: str, option: str) -> str:
        """Get a configuration option.
        
        Args:
            section (str): The section containing the option.
            option (str): The option to retrieve.
        
        Returns:
            str: The value of the option.
        
        Raises:
            ValueError: If the option or section is not found.
        """
        try:
            return self.config.get(section, option)
        except configparser.NoOptionError:
            raise ValueError(f"Option '{option}' not found in section '{section}'.")
        except configparser.NoSectionError:
            raise ValueError(f"Section '{section}' not found in configuration.")
        
config = Config()