from converter_gui.main_window import MainWindow
from converter_gui.config import config
import sys
import logging

def main():
    """Main function to start the application."""
    if len(sys.argv) < 2: 
        print("Usage: converter-gui <config_file>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    config._load_config(config_file)
    
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    logging.basicConfig(
        level=level_map[config.get("logging", "level")],  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
        handlers=[
            logging.StreamHandler(),  # Log to console
            logging.FileHandler("app.log")  # Log to a file
        ]
    )
    main_window = MainWindow()
    main_window.start()