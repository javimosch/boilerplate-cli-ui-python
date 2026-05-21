#!/usr/bin/env python3
"""
Entry point script for boilerplate-cli-ui-python.
This script avoids relative import issues by using absolute imports.
"""

import sys
import os

# Add project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Now import with absolute imports
from src.main import main

if __name__ == '__main__':
    main()