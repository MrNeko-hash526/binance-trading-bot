# Binance Futures Testnet Trading Bot

A simplified Python-based trading bot for Binance Futures Testnet that supports market orders, limit orders, and stop-limit orders with comprehensive logging and error handling.

## Features

- **Multiple Order Types**: Market, Limit, and Stop-Limit orders
- **Interactive CLI**: User-friendly command-line interface
- **Comprehensive Logging**: Separate logs for trades, errors, and system events
- **Risk Management**: Configurable limits and validation
- **Robust Error Handling**: Graceful handling of API errors and network issues
- **Flexible Configuration**: Environment variables, JSON config, and defaults
- **Testnet Support**: Safe testing environment with Binance Futures Testnet

## Quick Start

### 1. Prerequisites

- Python 3.7 or higher
- Binance Futures Testnet account ([Sign up here](https://testnet.binancefuture.com))

### 2. Installation

\`\`\`bash
# Clone or download the project
git clone <repository-url>
cd binance-trading-bot

# Install dependencies
pip install -r requirements.txt

# Run setup script
python setup.py
\`\`\`

### 3. Configuration

#### Option A: Using Environment Variables
\`\`\`bash
export BINANCE_API_KEY='your_api_key_here'
export BINANCE_API_SECRET='your_api_secret_here'
export BINANCE_TESTNET=true
\`\`\`

#### Option B: Using .env File
Create a `.env` file in the project root:
\`\`\`env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_TESTNET=true
DEFAULT_SYMBOL=BTCUSDT
LOG_LEVEL=INFO
\`\`\`

### 4. Run the Bot

\`\`\`bash
python main.py
\`\`\`

## Project Structure

```
binance-trading-bot/
├── main.py              # Entry point
├── bot.py               # Core trading bot class
├── cli.py               # Command-line interface
├── config.py            # Configuration management
├── logger.py            # Advanced logging system
├── utils.py             # Utility functions
├── setup.py             # Setup script
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── config.example.json  # Configuration template
├── logs/                # Log files directory
│   ├── trading_bot.log      # Main application log
│   ├── trades.log           # Trade-specific log
│   └── trading_bot_errors.log # Error log
└── README.md            # This file
\`\`\`

## Usage Guide

### Main Menu Options

1. **Place Market Order**: Execute immediate buy/sell at current market price
2. **Place Limit Order**: Set buy/sell order at specific price
3. **Place Stop-Limit Order**: Advanced order with stop price trigger
4. **View Account Info**: Display account balance and positions
5. **Exit**: Close the application

### Order Placement Flow

1. Select order type from main menu
2. Enter trading pair (default: BTCUSDT)
3. Choose order side (BUY/SELL)
4. Enter quantity
5. Enter price (for limit/stop-limit orders)
6. Enter stop price (for stop-limit orders only)
7. Confirm order details
8. Order is executed and logged

### Example Trading Session

```
BINANCE FUTURES TRADING BOT
==================================================
1. Place Market Order
2. Place Limit Order
3. Place Stop-Limit Order (Advanced)
4. View Account Info
5. Exit
==================================================

Select an option (1-5): 1

--- MARKET ORDER ---
Enter trading pair (default: BTCUSDT): 
Enter order side (BUY/SELL): BUY
Enter quantity: 0.001

ORDER CONFIRMATION
----------------------------------------
Type: MARKET
Symbol: BTCUSDT
Side: BUY
Quantity: 0.001
----------------------------------------
Confirm order? (y/n): y

Placing market order...

==================================================
ORDER EXECUTION SUMMARY
==================================================
Order ID: 123456789
Symbol: BTCUSDT
Side: BUY
Type: MARKET
Quantity: 0.001
Status: FILLED
Timestamp: 2024-01-15T10:30:45.123456
==================================================
\`\`\`

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BINANCE_API_KEY` | Your Binance API key | Required |
| `BINANCE_API_SECRET` | Your Binance API secret | Required |
| `BINANCE_TESTNET` | Use testnet (true/false) | true |
| `DEFAULT_SYMBOL` | Default trading pair | BTCUSDT |
| `LOG_LEVEL` | Logging level | INFO |
| `MAX_QUANTITY` | Maximum order quantity | 1000 |
| `MIN_QUANTITY` | Minimum order quantity | 0.001 |

### JSON Configuration

Create `config.json` for advanced settings:

\`\`\`json
{
  "trading": {
    "default_symbol": "BTCUSDT",
    "max_quantity": 1000,
    "min_quantity": 0.001,
    "supported_symbols": ["BTCUSDT", "ETHUSDT", "ADAUSDT"]
  },
  "risk_management": {
    "max_daily_trades": 50,
    "max_position_size": 100,
    "enable_stop_loss": true
  },
  "logging": {
    "log_level": "INFO",
    "max_log_size": 10485760,
    "log_backup_count": 5
  }
}
\`\`\`

## Logging

The bot creates three types of logs in the `logs/` directory:

### 1. Main Application Log (`trading_bot.log`)
- System events and general application flow
- API requests and responses
- Configuration changes
- User interactions

### 2. Trade Log (`trades.log`)
- Structured JSON format for easy parsing
- All order executions with complete details
- Trade timestamps and status updates

### 3. Error Log (`trading_bot_errors.log`)
- Detailed error information with stack traces
- API errors and network issues
- Configuration and validation errors

### Log Rotation
- Logs automatically rotate when they reach 10MB
- Keeps 5 backup files by default
- Configurable via environment variables or config file

## API Integration

### Supported Endpoints
- `futures_account()` - Account information
- `futures_create_order()` - Order placement
- `futures_exchange_info()` - Symbol information

### Error Handling
- **BinanceAPIException**: API-specific errors (rate limits, invalid parameters)
- **BinanceOrderException**: Order-specific errors (insufficient balance, invalid symbol)
- **Network Errors**: Connection timeouts and network issues
- **Validation Errors**: Input validation and parameter checking

## Risk Management

### Built-in Protections
- Order parameter validation
- Symbol existence verification
- Quantity and price range checks
- Configurable daily trade limits
- Position size limits

### Customizable Limits
\`\`\`python
# In config.json
"risk_management": {
  "max_daily_trades": 50,
  "max_position_size": 100,
  "enable_stop_loss": true,
  "stop_loss_percentage": 2.0,
  "take_profit_percentage": 5.0
}
\`\`\`

## Development

### Adding New Features

1. **New Order Types**: Extend the `BasicBot` class in `bot.py`
2. **CLI Enhancements**: Modify `cli.py` for new user interactions
3. **Configuration Options**: Update `config.py` and example files
4. **Logging**: Use the logging system in `logger.py`

### Code Structure

\`\`\`python
# Example: Adding a new order type
def place_trailing_stop_order(self, symbol, side, quantity, callback_rate):
    try:
        # Log the attempt
        log_system_event("Placing trailing stop order", {
            "symbol": symbol, "side": side, "quantity": quantity
        })
        
        # Place order via Binance API
        order = self.client.futures_create_order(
            symbol=symbol,
            side=side,
            type='TRAILING_STOP_MARKET',
            quantity=quantity,
            callbackRate=callback_rate
        )
        
        # Log successful trade
        log_trade(order_details, "TRAILING_STOP_ORDER")
        
        return order_details
        
    except Exception as e:
        log_error(e, "place_trailing_stop_order")
        raise
\`\`\`

## Troubleshooting

### Common Issues

#### 1. API Connection Errors
\`\`\`
Error: Invalid API key or secret
\`\`\`
**Solution**: Verify your API credentials in `.env` file or environment variables

#### 2. Symbol Not Found
\`\`\`
Error: Invalid symbol: INVALID
\`\`\`
**Solution**: Use valid Binance Futures symbols (e.g., BTCUSDT, ETHUSDT)

#### 3. Insufficient Balance
\`\`\`
Error: Account has insufficient balance
\`\`\`
**Solution**: Check your testnet account balance and reduce order quantity

#### 4. Rate Limit Exceeded
\`\`\`
Error: Too many requests
\`\`\`
**Solution**: Wait a few minutes before placing more orders

### Debug Mode

Enable debug logging for detailed troubleshooting:

\`\`\`bash
export LOG_LEVEL=DEBUG
python main.py
\`\`\`

### Log Analysis

Check specific log files for issues:

\`\`\`bash
# View recent trades
tail -f logs/trades.log

# Check for errors
tail -f logs/trading_bot_errors.log

# Monitor all activity
tail -f logs/trading_bot.log
\`\`\`

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use testnet** for development and testing
3. **Set appropriate permissions** on your Binance API key (Futures trading only)
4. **Monitor logs** for suspicious activity
5. **Use environment variables** for sensitive configuration
6. **Regularly rotate** API keys

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

## License

This project is for educational purposes only. Use at your own risk.

## Disclaimer

This trading bot is designed for educational and testing purposes using Binance Futures Testnet. 

**Important Warnings:**
- Never use this bot with real money without thorough testing
- Cryptocurrency trading involves significant risk
- Past performance does not guarantee future results
- Always test thoroughly on testnet before considering live trading
- The authors are not responsible for any financial losses

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review log files for error details
3. Ensure your configuration is correct
4. Verify your Binance Testnet account is properly set up

## Changelog

### v1.0.0
- Initial release
- Market, limit, and stop-limit order support
- Interactive CLI interface
- Comprehensive logging system
- Flexible configuration management
- Risk management features
