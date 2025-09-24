# API Documentation

This document describes the internal API structure and methods of the Binance Futures Trading Bot.

## Core Classes

### BasicBot Class

The main trading bot class that handles all Binance API interactions.

#### Constructor

\`\`\`python
BasicBot(api_key: str, api_secret: str, testnet: bool = True)
\`\`\`

**Parameters:**
- `api_key` (str): Binance API key
- `api_secret` (str): Binance API secret  
- `testnet` (bool): Whether to use testnet (default: True)

**Raises:**
- `Exception`: If client initialization fails

#### Methods

##### get_account_info()

\`\`\`python
get_account_info() -> Dict[str, Any]
\`\`\`

Retrieves futures account information including balance and positions.

**Returns:**
- `Dict[str, Any]`: Account information from Binance API

**Raises:**
- `BinanceAPIException`: API-related errors
- `Exception`: Unexpected errors

**Example Response:**
\`\`\`python
{
    'totalWalletBalance': '10000.00000000',
    'totalUnrealizedProfit': '0.00000000',
    'totalMarginBalance': '10000.00000000',
    'availableBalance': '10000.00000000',
    'positions': [...]
}
\`\`\`

##### place_market_order()

\`\`\`python
place_market_order(symbol: str, side: str, quantity: float) -> Dict[str, Any]
\`\`\`

Places a market order for immediate execution.

**Parameters:**
- `symbol` (str): Trading pair (e.g., 'BTCUSDT')
- `side` (str): Order side ('BUY' or 'SELL')
- `quantity` (float): Order quantity

**Returns:**
- `Dict[str, Any]`: Formatted order details

**Raises:**
- `BinanceOrderException`: Order-specific errors
- `BinanceAPIException`: API-related errors
- `Exception`: Unexpected errors

**Example Response:**
\`\`\`python
{
    'orderId': 123456789,
    'symbol': 'BTCUSDT',
    'side': 'BUY',
    'type': 'MARKET',
    'quantity': '0.001',
    'status': 'FILLED',
    'timestamp': '2024-01-15T10:30:45.123456'
}
\`\`\`

##### place_limit_order()

\`\`\`python
place_limit_order(symbol: str, side: str, quantity: float, price: float) -> Dict[str, Any]
\`\`\`

Places a limit order at a specific price.

**Parameters:**
- `symbol` (str): Trading pair (e.g., 'BTCUSDT')
- `side` (str): Order side ('BUY' or 'SELL')
- `quantity` (float): Order quantity
- `price` (float): Limit price

**Returns:**
- `Dict[str, Any]`: Formatted order details

**Example Response:**
\`\`\`python
{
    'orderId': 123456789,
    'symbol': 'BTCUSDT',
    'side': 'BUY',
    'type': 'LIMIT',
    'quantity': '0.001',
    'price': '45000.00',
    'status': 'NEW',
    'timestamp': '2024-01-15T10:30:45.123456'
}
\`\`\`

##### place_stop_limit_order()

\`\`\`python
place_stop_limit_order(symbol: str, side: str, quantity: float, price: float, stop_price: float) -> Dict[str, Any]
\`\`\`

Places a stop-limit order with trigger price.

**Parameters:**
- `symbol` (str): Trading pair
- `side` (str): Order side ('BUY' or 'SELL')
- `quantity` (float): Order quantity
- `price` (float): Limit price
- `stop_price` (float): Stop trigger price

**Returns:**
- `Dict[str, Any]`: Formatted order details

##### validate_order_params()

\`\`\`python
validate_order_params(symbol: str, quantity: float, price: Optional[float] = None) -> bool
\`\`\`

Validates order parameters before placement.

**Parameters:**
- `symbol` (str): Trading pair
- `quantity` (float): Order quantity
- `price` (float, optional): Order price

**Returns:**
- `bool`: True if valid, False otherwise

### ConfigManager Class

Handles configuration loading and management.

#### Constructor

\`\`\`python
ConfigManager(config_file: str = "config.json", env_file: str = ".env")
\`\`\`

#### Methods

##### get()

\`\`\`python
get(path: str, default: Any = None) -> Any
\`\`\`

Get configuration value using dot notation.

**Parameters:**
- `path` (str): Configuration path (e.g., 'api.testnet')
- `default` (Any): Default value if not found

**Example:**
\`\`\`python
config = ConfigManager()
testnet = config.get('api.testnet', True)
symbol = config.get('trading.default_symbol', 'BTCUSDT')
\`\`\`

##### set()

\`\`\`python
set(path: str, value: Any)
\`\`\`

Set configuration value using dot notation.

##### get_api_credentials()

\`\`\`python
get_api_credentials() -> tuple
\`\`\`

Get API credentials from configuration.

**Returns:**
- `tuple`: (api_key, api_secret)

**Raises:**
- `ValueError`: If credentials not found

##### validate_config()

\`\`\`python
validate_config() -> bool
\`\`\`

Validate configuration completeness and correctness.

**Returns:**
- `bool`: True if valid, False otherwise

### TradingBotLogger Class

Advanced logging system with multiple handlers.

#### Constructor

\`\`\`python
TradingBotLogger(
    log_file: str = "trading_bot.log",
    error_log_file: str = "trading_bot_errors.log", 
    trade_log_file: str = "trades.log",
    log_level: str = "INFO",
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5
)
\`\`\`

#### Methods

##### log_trade()

\`\`\`python
log_trade(order_details: dict, trade_type: str = "ORDER")
\`\`\`

Log trade information in structured JSON format.

##### log_error()

\`\`\`python
log_error(error: Exception, context: str = "")
\`\`\`

Log error with context and stack trace.

##### log_system_event()

\`\`\`python
log_system_event(event: str, details: dict = None)
\`\`\`

Log system events like startup, shutdown, configuration changes.

## Utility Functions

### Validation Functions

#### validate_input()

\`\`\`python
validate_input(prompt: str, input_type: type, min_value: float = None, max_value: float = None)
\`\`\`

Validate user input with type checking and range validation.

#### validate_trading_pair()

\`\`\`python
validate_trading_pair(symbol: str) -> str
\`\`\`

Validate and format trading pair symbol.

#### validate_order_side()

\`\`\`python
validate_order_side(side: str) -> str
\`\`\`

Validate order side (BUY/SELL).

#### validate_order_type()

\`\`\`python
validate_order_type(order_type: str) -> str
\`\`\`

Validate order type (MARKET/LIMIT/STOP-LIMIT).

### Display Functions

#### print_order_summary()

\`\`\`python
print_order_summary(order_details: Dict[str, Any])
\`\`\`

Print formatted order execution summary.

## Error Handling

### Exception Types

#### BinanceAPIException
- API-related errors (rate limits, authentication)
- Network connectivity issues
- Server-side errors

#### BinanceOrderException  
- Order-specific errors (insufficient balance, invalid symbol)
- Order parameter validation failures
- Market-specific restrictions

#### ValueError
- Configuration validation errors
- Input parameter errors
- Type conversion errors

### Error Response Format

\`\`\`python
{
    'error_type': 'BinanceAPIException',
    'error_code': -1021,
    'error_message': 'Timestamp for this request is outside of the recvWindow.',
    'context': 'place_market_order',
    'timestamp': '2024-01-15T10:30:45.123456'
}
\`\`\`

## Logging Format

### Trade Log Format (JSON)

\`\`\`json
{
    "timestamp": "2024-01-15T10:30:45.123456",
    "type": "MARKET_ORDER",
    "order_id": 123456789,
    "symbol": "BTCUSDT",
    "side": "BUY",
    "order_type": "MARKET",
    "quantity": "0.001",
    "status": "FILLED"
}
\`\`\`

### System Event Log Format

\`\`\`
2024-01-15 10:30:45,123 - trading_bot - INFO - main:45 - System Event: Bot initialized - Details: {"testnet": true, "timestamp": "2024-01-15T10:30:45.123456"}
\`\`\`

### Error Log Format

\`\`\`
2024-01-15 10:30:45,123 - errors - ERROR - place_market_order:123
Message: API Error: Invalid symbol
Module: bot
Path: /path/to/bot.py
---
\`\`\`

## Rate Limiting

### Binance API Limits
- **Order Rate**: 300 requests per minute
- **Request Weight**: 1200 per minute
- **Raw Requests**: 6000 per 5 minutes

### Bot Implementation
- Automatic retry with exponential backoff
- Rate limit buffer configuration
- Request weight tracking
- Graceful degradation on limits

## Configuration Schema

### Complete Configuration Structure

\`\`\`json
{
    "api": {
        "key": "string",
        "secret": "string", 
        "testnet": "boolean",
        "timeout": "number",
        "retry_attempts": "number",
        "rate_limit_buffer": "number"
    },
    "trading": {
        "default_symbol": "string",
        "max_quantity": "number",
        "min_quantity": "number",
        "supported_symbols": ["string"],
        "default_order_type": "string"
    },
    "risk_management": {
        "max_daily_trades": "number",
        "max_position_size": "number", 
        "enable_stop_loss": "boolean",
        "stop_loss_percentage": "number",
        "take_profit_percentage": "number"
    },
    "logging": {
        "log_level": "string",
        "max_log_size": "number",
        "log_backup_count": "number",
        "enable_trade_logging": "boolean",
        "enable_error_logging": "boolean"
    },
    "ui": {
        "show_confirmations": "boolean",
        "auto_refresh_account": "boolean",
        "display_precision": "number"
    }
}
\`\`\`

## Extension Points

### Adding New Order Types

1. **Extend BasicBot class**:
\`\`\`python
def place_custom_order(self, symbol, side, quantity, **kwargs):
    # Implementation
    pass
\`\`\`

2. **Add CLI menu option**:
\`\`\`python
def place_custom_order_cli(self):
    # CLI implementation
    pass
\`\`\`

3. **Update logging**:
\`\`\`python
log_trade(order_details, "CUSTOM_ORDER")
\`\`\`

### Adding New Validation Rules

\`\`\`python
def validate_custom_params(self, **params) -> bool:
    # Custom validation logic
    return True
\`\`\`

### Custom Configuration Sections

\`\`\`python
# In ConfigManager
def get_custom_config(self) -> Dict[str, Any]:
    return self.get('custom_section', {})
\`\`\`

This API documentation provides a comprehensive reference for developers working with or extending the trading bot codebase.
