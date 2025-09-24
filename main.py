#!/usr/bin/env python3
"""
Binance Futures Testnet Trading Bot
A simplified trading bot for educational purposes.

Usage:
    python main.py

Make sure to set your API credentials as environment variables:
    export BINANCE_API_KEY='your_api_key'
    export BINANCE_API_SECRET='your_api_secret'
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli import main

if __name__ == "__main__":
    main()
