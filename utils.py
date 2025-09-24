import logging
import os
from datetime import datetime
from typing import Dict, Any
import json

def setup_logging(log_file: str = "trading_bot.log", log_level: int = logging.INFO):
    """
    Set up logging configuration for the trading bot.
    
    Args:
        log_file (str): Path to log file
        log_level (int): Logging level
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file) if os.path.dirname(log_file) else '.'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configure logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    logging.info("Logging system initialized")

def validate_input(prompt: str, input_type: type, min_value: float = None, max_value: float = None):
    """
    Validate user input with type checking and range validation.
    
    Args:
        prompt (str): Input prompt message
        input_type (type): Expected input type (int, float, str)
        min_value (float, optional): Minimum allowed value
        max_value (float, optional): Maximum allowed value
        
    Returns:
        Validated input value
    """
    while True:
        try:
            user_input = input(prompt).strip()
            
            if input_type == str:
                if user_input:
                    return user_input.upper()
                else:
                    print("Input cannot be empty. Please try again.")
                    continue
            
            # Convert to numeric type
            value = input_type(user_input)
            
            # Check range if specified
            if min_value is not None and value < min_value:
                print(f"Value must be at least {min_value}. Please try again.")
                continue
            
            if max_value is not None and value > max_value:
                print(f"Value must be at most {max_value}. Please try again.")
                continue
            
            return value
            
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            exit(0)

def validate_trading_pair(symbol: str) -> str:
    """
    Validate and format trading pair symbol.
    
    Args:
        symbol (str): Trading pair symbol
        
    Returns:
        str: Formatted symbol
    """
    symbol = symbol.upper().strip()
    
    # Basic validation - should end with USDT for futures
    if not symbol.endswith('USDT'):
        print(f"Warning: {symbol} doesn't end with USDT. This might not be a valid futures pair.")
    
    return symbol

def validate_order_side(side: str) -> str:
    """
    Validate order side (buy/sell).
    
    Args:
        side (str): Order side
        
    Returns:
        str: Validated side ('BUY' or 'SELL')
    """
    side = side.upper().strip()
    
    if side not in ['BUY', 'SELL']:
        raise ValueError(f"Invalid order side: {side}. Must be 'BUY' or 'SELL'")
    
    return side

def validate_order_type(order_type: str) -> str:
    """
    Validate order type.
    
    Args:
        order_type (str): Order type
        
    Returns:
        str: Validated order type
    """
    order_type = order_type.upper().strip()
    
    valid_types = ['MARKET', 'LIMIT', 'STOP-LIMIT']
    if order_type not in valid_types:
        raise ValueError(f"Invalid order type: {order_type}. Must be one of {valid_types}")
    
    return order_type

def print_order_summary(order_details: Dict[str, Any]):
    """
    Print a formatted order summary.
    
    Args:
        order_details (dict): Order details dictionary
    """
    print("\n" + "="*50)
    print("ORDER EXECUTION SUMMARY")
    print("="*50)
    print(f"Order ID: {order_details.get('orderId', 'N/A')}")
    print(f"Symbol: {order_details.get('symbol', 'N/A')}")
    print(f"Side: {order_details.get('side', 'N/A')}")
    print(f"Type: {order_details.get('type', 'N/A')}")
    print(f"Quantity: {order_details.get('quantity', 'N/A')}")
    
    if 'price' in order_details:
        print(f"Price: {order_details['price']}")
    
    if 'stopPrice' in order_details:
        print(f"Stop Price: {order_details['stopPrice']}")
    
    print(f"Status: {order_details.get('status', 'N/A')}")
    print(f"Timestamp: {order_details.get('timestamp', 'N/A')}")
    print("="*50)

def load_config(config_file: str = "config.json") -> Dict[str, Any]:
    """
    Load configuration from JSON file.
    
    Args:
        config_file (str): Path to config file
        
    Returns:
        dict: Configuration dictionary
    """
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
            logging.info(f"Configuration loaded from {config_file}")
            return config
        else:
            logging.warning(f"Config file {config_file} not found")
            return {}
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        return {}

def save_config(config: Dict[str, Any], config_file: str = "config.json"):
    """
    Save configuration to JSON file.
    
    Args:
        config (dict): Configuration dictionary
        config_file (str): Path to config file
    """
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        logging.info(f"Configuration saved to {config_file}")
    except Exception as e:
        logging.error(f"Error saving config: {e}")
