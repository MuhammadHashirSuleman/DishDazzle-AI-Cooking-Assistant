#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DishDazzle - AI-powered desktop recipe assistant
Main application entry point
"""

import sys
import logging
from PyQt5.QtWidgets import QApplication

from ui import MainWindow
from utils import setup_logging, load_config
from database import initialize_database


def main():
    """Main application entry point"""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting DishDazzle application")
    
    # Load configuration
    config = load_config()
    
    # Initialize database
    initialize_database()
    
    # Create and start Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("DishDazzle")
    app.setStyle("Fusion")  # Use Fusion style for consistent look across platforms
    
    # Create and show main window
    main_window = MainWindow(config)
    main_window.show()
    
    # Start application event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()