import os
import json
from typing import Dict, Any, Optional, List
import logging
from pathlib import Path

class ConfigManager:
    """
    Comprehensive configuration manager for the trading bot.
    Handles loading from multiple sources with priority: ENV > JSON > defaults.
    """
    
    def __init__(self, config_file: str = "config.json", env_file: str = ".env"):
        self.config_file = config_file
        self.env_file = env_file
        self.config = {}
        self.defaults = self._get_default_config()
        
        # Load configuration in priority order
        self.load_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration values."""
        return {
            "api": {
                "testnet": True,
                "timeout": 30,
                "retry_attempts": 3,
                "rate_limit_buffer": 0.1
            },
            "trading": {
                "default_symbol": "BTCUSDT",
                "max_quantity": 1000,
                "min_quantity": 0.001,
                "supported_symbols": ["BTCUSDT", "ETHUSDT", "ADAUSDT", "DOTUSDT"],
                "default_order_type": "LIMIT"
            },
            "risk_management": {
                "max_daily_trades": 50,
                "max_position_size": 100,
                "enable_stop_loss": True,
                "stop_loss_percentage": 2.0,
                "take_profit_percentage": 5.0
            },
            "logging": {
                "log_level": "INFO",
                "max_log_size": 10 * 1024 * 1024,  # 10MB
                "log_backup_count": 5,
                "enable_trade_logging": True,
                "enable_error_logging": True
            },
            "ui": {
                "show_confirmations": True,
                "auto_refresh_account": False,
                "display_precision": 8
            }
        }
    
    def load_config(self):
        """Load configuration from all sources."""
        # Start with defaults
        self.config = self.defaults.copy()
        
        # Load from JSON file if exists
        self._load_from_json()
        
        # Load from environment file if exists
        self._load_from_env_file()
        
        # Override with environment variables
        self._load_from_env_vars()
        
        logging.info("Configuration loaded successfully")
    
    def _load_from_json(self):
        """Load configuration from JSON file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    json_config = json.load(f)
                
                # Deep merge with existing config
                self._deep_merge(self.config, json_config)
                logging.info(f"Configuration loaded from {self.config_file}")
                
            except Exception as e:
                logging.error(f"Error loading JSON config: {e}")
    
    def _load_from_env_file(self):
        """Load configuration from .env file."""
        if os.path.exists(self.env_file):
            try:
                with open(self.env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            os.environ[key.strip()] = value.strip()
                
                logging.info(f"Environment variables loaded from {self.env_file}")
                
            except Exception as e:
                logging.error(f"Error loading .env file: {e}")
    
    def _load_from_env_vars(self):
        """Load configuration from environment variables."""
        env_mappings = {
            # API Configuration
            'BINANCE_API_KEY': ('api', 'key'),
            'BINANCE_API_SECRET': ('api', 'secret'),
            'BINANCE_TESTNET': ('api', 'testnet'),
            'API_TIMEOUT': ('api', 'timeout'),
            'API_RETRY_ATTEMPTS': ('api', 'retry_attempts'),
            
            # Trading Configuration
            'DEFAULT_SYMBOL': ('trading', 'default_symbol'),
            'MAX_QUANTITY': ('trading', 'max_quantity'),
            'MIN_QUANTITY': ('trading', 'min_quantity'),
            'DEFAULT_ORDER_TYPE': ('trading', 'default_order_type'),
            
            # Risk Management
            'MAX_DAILY_TRADES': ('risk_management', 'max_daily_trades'),
            'MAX_POSITION_SIZE': ('risk_management', 'max_position_size'),
            'ENABLE_STOP_LOSS': ('risk_management', 'enable_stop_loss'),
            'STOP_LOSS_PERCENTAGE': ('risk_management', 'stop_loss_percentage'),
            'TAKE_PROFIT_PERCENTAGE': ('risk_management', 'take_profit_percentage'),
            
            # Logging Configuration
            'LOG_LEVEL': ('logging', 'log_level'),
            'MAX_LOG_SIZE': ('logging', 'max_log_size'),
            'LOG_BACKUP_COUNT': ('logging', 'log_backup_count'),
            
            # UI Configuration
            'SHOW_CONFIRMATIONS': ('ui', 'show_confirmations'),
            'AUTO_REFRESH_ACCOUNT': ('ui', 'auto_refresh_account'),
            'DISPLAY_PRECISION': ('ui', 'display_precision')
        }
        
        for env_key, (section, config_key) in env_mappings.items():
            env_value = os.getenv(env_key)
            if env_value is not None:
                # Convert value to appropriate type
                converted_value = self._convert_env_value(env_value)
                
                # Set in config
                if section not in self.config:
                    self.config[section] = {}
                self.config[section][config_key] = converted_value
    
    def _convert_env_value(self, value: str) -> Any:
        """Convert environment variable string to appropriate type."""
        # Boolean conversion
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        
        # Integer conversion
        try:
            if '.' not in value:
                return int(value)
        except ValueError:
            pass
        
        # Float conversion
        try:
            return float(value)
        except ValueError:
            pass
        
        # Return as string
        return value
    
    def _deep_merge(self, base: Dict, update: Dict):
        """Deep merge two dictionaries."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def get(self, path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            path (str): Configuration path (e.g., 'api.testnet', 'trading.default_symbol')
            default (Any): Default value if not found
            
        Returns:
            Configuration value or default
        """
        keys = path.split('.')
        current = self.config
        
        try:
            for key in keys:
                current = current[key]
            return current
        except (KeyError, TypeError):
            return default
    
    def set(self, path: str, value: Any):
        """
        Set configuration value using dot notation.
        
        Args:
            path (str): Configuration path
            value (Any): Value to set
        """
        keys = path.split('.')
        current = self.config
        
        # Navigate to parent
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Set value
        current[keys[-1]] = value
    
    def save_config(self, config_file: Optional[str] = None):
        """
        Save current configuration to JSON file (excluding sensitive data).
        
        Args:
            config_file (str, optional): Config file path
        """
        file_path = config_file or self.config_file
        
        try:
            # Create safe config (without sensitive data)
            safe_config = self._create_safe_config()
            
            with open(file_path, 'w') as f:
                json.dump(safe_config, f, indent=2)
            
            logging.info(f"Configuration saved to {file_path}")
            
        except Exception as e:
            logging.error(f"Error saving config: {e}")
    
    def _create_safe_config(self) -> Dict[str, Any]:
        """Create configuration without sensitive data."""
        safe_config = {}
        
        for section, values in self.config.items():
            if section == 'api':
                # Exclude sensitive API credentials
                safe_config[section] = {
                    k: v for k, v in values.items() 
                    if k not in ['key', 'secret']
                }
            else:
                safe_config[section] = values.copy()
        
        return safe_config
    
    def get_api_credentials(self) -> tuple:
        """Get API credentials from configuration."""
        api_key = self.get('api.key')
        api_secret = self.get('api.secret')
        
        if not api_key or not api_secret:
            raise ValueError(
                "API credentials not found. Please set BINANCE_API_KEY and "
                "BINANCE_API_SECRET environment variables or add them to your config."
            )
        
        return api_key, api_secret
    
    def is_testnet(self) -> bool:
        """Check if testnet mode is enabled."""
        return self.get('api.testnet', True)
    
    def get_default_symbol(self) -> str:
        """Get default trading symbol."""
        return self.get('trading.default_symbol', 'BTCUSDT')
    
    def get_supported_symbols(self) -> List[str]:
        """Get list of supported trading symbols."""
        return self.get('trading.supported_symbols', ['BTCUSDT', 'ETHUSDT'])
    
    def get_risk_limits(self) -> Dict[str, Any]:
        """Get risk management limits."""
        return {
            'max_daily_trades': self.get('risk_management.max_daily_trades', 50),
            'max_position_size': self.get('risk_management.max_position_size', 100),
            'max_quantity': self.get('trading.max_quantity', 1000),
            'min_quantity': self.get('trading.min_quantity', 0.001)
        }
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        return {
            'log_level': self.get('logging.log_level', 'INFO'),
            'max_log_size': self.get('logging.max_log_size', 10 * 1024 * 1024),
            'log_backup_count': self.get('logging.log_backup_count', 5),
            'enable_trade_logging': self.get('logging.enable_trade_logging', True),
            'enable_error_logging': self.get('logging.enable_error_logging', True)
        }
    
    def validate_config(self) -> bool:
        """Validate that required configuration is present and valid."""
        try:
            # Check API credentials
            self.get_api_credentials()
            
            # Validate numeric limits
            limits = self.get_risk_limits()
            for key, value in limits.items():
                if not isinstance(value, (int, float)) or value <= 0:
                    logging.error(f"Invalid {key}: {value}")
                    return False
            
            # Validate symbol
            default_symbol = self.get_default_symbol()
            if not isinstance(default_symbol, str) or len(default_symbol) < 3:
                logging.error(f"Invalid default symbol: {default_symbol}")
                return False
            
            # Validate log level
            log_level = self.get('logging.log_level', 'INFO')
            if log_level.upper() not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
                logging.error(f"Invalid log level: {log_level}")
                return False
            
            return True
            
        except ValueError as e:
            logging.error(f"Configuration validation failed: {e}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error during validation: {e}")
            return False
    
    def create_example_files(self):
        """Create example configuration files."""
        try:
            # Create example .env file
            env_example_path = ".env.example"
            if not os.path.exists(env_example_path):
                env_content = """# Binance API Configuration
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_TESTNET=true

# Trading Configuration
DEFAULT_SYMBOL=BTCUSDT
MAX_QUANTITY=1000
MIN_QUANTITY=0.001

# Logging Configuration
LOG_LEVEL=INFO
MAX_LOG_SIZE=10485760
LOG_BACKUP_COUNT=5

# Risk Management
MAX_DAILY_TRADES=50
MAX_POSITION_SIZE=100
ENABLE_STOP_LOSS=true
"""
                with open(env_example_path, 'w') as f:
                    f.write(env_content)
                print(f"Created {env_example_path}")
            
            # Create example config.json file
            config_example_path = "config.example.json"
            if not os.path.exists(config_example_path):
                with open(config_example_path, 'w') as f:
                    json.dump(self.defaults, f, indent=2)
                print(f"Created {config_example_path}")
            
            print("\nSetup Instructions:")
            print("1. Copy .env.example to .env and add your API credentials")
            print("2. Copy config.example.json to config.json and customize as needed")
            print("3. Set environment variables or edit the files directly")
            
        except Exception as e:
            logging.error(f"Error creating example files: {e}")
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of current configuration (safe for logging)."""
        return {
            'api': {
                'testnet': self.is_testnet(),
                'timeout': self.get('api.timeout'),
                'has_credentials': bool(self.get('api.key') and self.get('api.secret'))
            },
            'trading': {
                'default_symbol': self.get_default_symbol(),
                'supported_symbols_count': len(self.get_supported_symbols())
            },
            'risk_limits': self.get_risk_limits(),
            'logging': self.get_logging_config()
        }

def create_config_files():
    """Utility function to create example configuration files."""
    config_manager = ConfigManager()
    config_manager.create_example_files()

if __name__ == "__main__":
    create_config_files()
