import logging
import logging.handlers
import os
from datetime import datetime
from typing import Optional
import json

class TradingBotLogger:
    """
    Advanced logging system for the trading bot with multiple handlers and formatters.
    """
    
    def __init__(self, 
                 log_file: str = "trading_bot.log",
                 error_log_file: str = "trading_bot_errors.log",
                 trade_log_file: str = "trades.log",
                 log_level: str = "INFO",
                 max_bytes: int = 10 * 1024 * 1024,  # 10MB
                 backup_count: int = 5):
        """
        Initialize the logging system.
        
        Args:
            log_file (str): Main log file path
            error_log_file (str): Error-specific log file path
            trade_log_file (str): Trade-specific log file path
            log_level (str): Logging level
            max_bytes (int): Maximum log file size before rotation
            backup_count (int): Number of backup files to keep
        """
        self.log_file = log_file
        self.error_log_file = error_log_file
        self.trade_log_file = trade_log_file
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        
        # Create logs directory
        self.logs_dir = "logs"
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Setup loggers
        self.setup_main_logger()
        self.setup_trade_logger()
        self.setup_error_logger()
    
    def setup_main_logger(self):
        """Setup the main application logger."""
        # Main logger
        self.main_logger = logging.getLogger('trading_bot')
        self.main_logger.setLevel(self.log_level)
        
        # Clear existing handlers
        self.main_logger.handlers.clear()
        
        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            os.path.join(self.logs_dir, self.log_file),
            maxBytes=self.max_bytes,
            backupCount=self.backup_count
        )
        file_handler.setLevel(self.log_level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        file_handler.setFormatter(detailed_formatter)
        console_handler.setFormatter(simple_formatter)
        
        # Add handlers
        self.main_logger.addHandler(file_handler)
        self.main_logger.addHandler(console_handler)
        
        # Prevent propagation to root logger
        self.main_logger.propagate = False
    
    def setup_trade_logger(self):
        """Setup the trade-specific logger."""
        self.trade_logger = logging.getLogger('trades')
        self.trade_logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        self.trade_logger.handlers.clear()
        
        # Trade file handler
        trade_handler = logging.handlers.RotatingFileHandler(
            os.path.join(self.logs_dir, self.trade_log_file),
            maxBytes=self.max_bytes,
            backupCount=self.backup_count
        )
        trade_handler.setLevel(logging.INFO)
        
        # Trade formatter (JSON format for easy parsing)
        trade_formatter = logging.Formatter('%(asctime)s - %(message)s')
        trade_handler.setFormatter(trade_formatter)
        
        self.trade_logger.addHandler(trade_handler)
        self.trade_logger.propagate = False
    
    def setup_error_logger(self):
        """Setup the error-specific logger."""
        self.error_logger = logging.getLogger('errors')
        self.error_logger.setLevel(logging.ERROR)
        
        # Clear existing handlers
        self.error_logger.handlers.clear()
        
        # Error file handler
        error_handler = logging.handlers.RotatingFileHandler(
            os.path.join(self.logs_dir, self.error_log_file),
            maxBytes=self.max_bytes,
            backupCount=self.backup_count
        )
        error_handler.setLevel(logging.ERROR)
        
        # Error formatter with more details
        error_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d\n'
            'Message: %(message)s\n'
            'Module: %(module)s\n'
            'Path: %(pathname)s\n'
            '---'
        )
        error_handler.setFormatter(error_formatter)
        
        self.error_logger.addHandler(error_handler)
        self.error_logger.propagate = False
    
    def log_trade(self, order_details: dict, trade_type: str = "ORDER"):
        """
        Log trade information in structured format.
        
        Args:
            order_details (dict): Order details from API response
            trade_type (str): Type of trade log entry
        """
        trade_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": trade_type,
            "order_id": order_details.get('orderId'),
            "symbol": order_details.get('symbol'),
            "side": order_details.get('side'),
            "order_type": order_details.get('type'),
            "quantity": order_details.get('quantity'),
            "price": order_details.get('price'),
            "status": order_details.get('status'),
            "stop_price": order_details.get('stopPrice')
        }
        
        # Remove None values
        trade_entry = {k: v for k, v in trade_entry.items() if v is not None}
        
        self.trade_logger.info(json.dumps(trade_entry))
    
    def log_api_request(self, endpoint: str, params: dict, response_status: str):
        """
        Log API request details.
        
        Args:
            endpoint (str): API endpoint
            params (dict): Request parameters
            response_status (str): Response status
        """
        self.main_logger.info(
            f"API Request - Endpoint: {endpoint}, "
            f"Params: {params}, Status: {response_status}"
        )
    
    def log_error(self, error: Exception, context: str = ""):
        """
        Log error with context.
        
        Args:
            error (Exception): The exception that occurred
            context (str): Additional context about the error
        """
        error_msg = f"Error in {context}: {str(error)}" if context else str(error)
        
        self.error_logger.error(error_msg, exc_info=True)
        self.main_logger.error(error_msg)
    
    def log_system_event(self, event: str, details: dict = None):
        """
        Log system events like startup, shutdown, configuration changes.
        
        Args:
            event (str): Event description
            details (dict): Additional event details
        """
        msg = f"System Event: {event}"
        if details:
            msg += f" - Details: {json.dumps(details)}"
        
        self.main_logger.info(msg)
    
    def get_logger(self, name: str = 'trading_bot') -> logging.Logger:
        """
        Get a logger instance.
        
        Args:
            name (str): Logger name
            
        Returns:
            logging.Logger: Logger instance
        """
        if name == 'trades':
            return self.trade_logger
        elif name == 'errors':
            return self.error_logger
        else:
            return self.main_logger
    
    def set_log_level(self, level: str):
        """
        Change the logging level.
        
        Args:
            level (str): New logging level
        """
        new_level = getattr(logging, level.upper(), logging.INFO)
        self.main_logger.setLevel(new_level)
        
        # Update file handler level
        for handler in self.main_logger.handlers:
            if isinstance(handler, logging.handlers.RotatingFileHandler):
                handler.setLevel(new_level)
    
    def get_log_stats(self) -> dict:
        """
        Get statistics about log files.
        
        Returns:
            dict: Log file statistics
        """
        stats = {}
        
        log_files = [
            self.log_file,
            self.error_log_file,
            self.trade_log_file
        ]
        
        for log_file in log_files:
            file_path = os.path.join(self.logs_dir, log_file)
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                stats[log_file] = {
                    'size_bytes': stat.st_size,
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                }
            else:
                stats[log_file] = {'exists': False}
        
        return stats

# Global logger instance
_logger_instance: Optional[TradingBotLogger] = None

def get_logger_instance(config: dict = None) -> TradingBotLogger:
    """
    Get or create the global logger instance.
    
    Args:
        config (dict): Logger configuration
        
    Returns:
        TradingBotLogger: Logger instance
    """
    global _logger_instance
    
    if _logger_instance is None:
        if config:
            _logger_instance = TradingBotLogger(**config)
        else:
            _logger_instance = TradingBotLogger()
    
    return _logger_instance

def setup_logging(config: dict = None):
    """
    Setup the global logging system.
    
    Args:
        config (dict): Logger configuration
    """
    logger_instance = get_logger_instance(config)
    
    # Set the root logger to use our main logger
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(logger_instance.main_logger.handlers[0])  # File handler
    root_logger.setLevel(logger_instance.log_level)
    
    logger_instance.log_system_event("Logging system initialized", config)

# Convenience functions
def log_trade(order_details: dict, trade_type: str = "ORDER"):
    """Log trade information."""
    get_logger_instance().log_trade(order_details, trade_type)

def log_error(error: Exception, context: str = ""):
    """Log error with context."""
    get_logger_instance().log_error(error, context)

def log_api_request(endpoint: str, params: dict, response_status: str):
    """Log API request."""
    get_logger_instance().log_api_request(endpoint, params, response_status)

def log_system_event(event: str, details: dict = None):
    """Log system event."""
    get_logger_instance().log_system_event(event, details)
