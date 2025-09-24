# Setup Guide

This guide will walk you through setting up the Binance Futures Testnet Trading Bot step by step.

## Prerequisites

### 1. Python Installation
- **Required**: Python 3.7 or higher
- **Recommended**: Python 3.9+

Check your Python version:
\`\`\`bash
python --version
# or
python3 --version
\`\`\`

If you need to install Python:
- **Windows**: Download from [python.org](https://python.org)
- **macOS**: Use Homebrew: `brew install python3`
- **Linux**: Use your package manager: `sudo apt install python3 python3-pip`

### 2. Binance Futures Testnet Account

1. Go to [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Sign up for a free account
3. Generate API credentials:
   - Go to API Management
   - Create New Key
   - **Important**: Enable "Futures" permissions
   - Save your API Key and Secret Key securely

## Installation Methods

### Method 1: Automated Setup (Recommended)

1. **Download the project**:
   \`\`\`bash
   # If using git
   git clone <repository-url>
   cd binance-trading-bot
   
   # Or download and extract the ZIP file
   \`\`\`

2. **Install dependencies**:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Run the setup script**:
   \`\`\`bash
   python setup.py
   \`\`\`
   
   The setup script will:
   - Check Python version compatibility
   - Verify all dependencies are installed
   - Create necessary directories
   - Generate example configuration files
   - Optionally set up your API credentials
   - Test the configuration

### Method 2: Manual Setup

1. **Install dependencies**:
   \`\`\`bash
   pip install python-binance python-dotenv
   \`\`\`

2. **Create directories**:
   \`\`\`bash
   mkdir logs
   \`\`\`

3. **Set up configuration** (choose one):

   **Option A: Environment Variables**
   \`\`\`bash
   export BINANCE_API_KEY='your_api_key_here'
   export BINANCE_API_SECRET='your_api_secret_here'
   export BINANCE_TESTNET=true
   \`\`\`

   **Option B: .env File**
   Create `.env` file:
   \`\`\`env
   BINANCE_API_KEY=your_api_key_here
   BINANCE_API_SECRET=your_api_secret_here
   BINANCE_TESTNET=true
   DEFAULT_SYMBOL=BTCUSDT
   LOG_LEVEL=INFO
   \`\`\`

## Configuration Details

### API Credentials Setup

#### Getting Your API Keys

1. **Login** to [Binance Futures Testnet](https://testnet.binancefuture.com)
2. **Navigate** to API Management (usually in account settings)
3. **Create New Key**:
   - Give it a descriptive name (e.g., "Trading Bot")
   - **Enable Futures Trading** permission
   - **Disable** withdrawal permissions (not needed)
4. **Save** both the API Key and Secret Key immediately
5. **Test** the connection using the testnet

#### Security Best Practices

- **Never share** your API keys
- **Never commit** API keys to version control
- **Use testnet** for development
- **Set minimal permissions** (Futures trading only)
- **Regularly rotate** your keys

### Configuration Files

#### .env File (Recommended for credentials)
\`\`\`env
# Required - Your Binance API credentials
BINANCE_API_KEY=your_actual_api_key_here
BINANCE_API_SECRET=your_actual_secret_here

# Optional - Trading settings
BINANCE_TESTNET=true
DEFAULT_SYMBOL=BTCUSDT
MAX_QUANTITY=1000
MIN_QUANTITY=0.001

# Optional - Logging settings
LOG_LEVEL=INFO
MAX_LOG_SIZE=10485760
LOG_BACKUP_COUNT=5

# Optional - Risk management
MAX_DAILY_TRADES=50
MAX_POSITION_SIZE=100
ENABLE_STOP_LOSS=true
\`\`\`

#### config.json (Optional for advanced settings)
\`\`\`json
{
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
    "enable_stop_loss": true,
    "stop_loss_percentage": 2.0,
    "take_profit_percentage": 5.0
  },
  "logging": {
    "log_level": "INFO",
    "max_log_size": 10485760,
    "log_backup_count": 5,
    "enable_trade_logging": true,
    "enable_error_logging": true
  },
  "api": {
    "testnet": true,
    "timeout": 30,
    "retry_attempts": 3,
    "rate_limit_buffer": 0.1
  },
  "ui": {
    "show_confirmations": true,
    "auto_refresh_account": false,
    "display_precision": 8
  }
}
\`\`\`

## Testing Your Setup

### 1. Configuration Test
\`\`\`bash
python -c "from config import ConfigManager; cm = ConfigManager(); print('✓ Config loaded') if cm.validate_config() else print('✗ Config invalid')"
\`\`\`

### 2. API Connection Test
\`\`\`bash
python main.py
\`\`\`

If successful, you should see:
\`\`\`
Connected to Binance Testnet successfully!
Account Balance: 10000.00000000 USDT
\`\`\`

### 3. Test Trade (Optional)
- Select option 1 (Market Order)
- Use BTCUSDT symbol
- Place a small BUY order (0.001 quantity)
- Check logs for successful execution

## Troubleshooting Setup Issues

### Common Problems

#### 1. Python Version Error
\`\`\`
Error: Python 3.7 or higher is required
\`\`\`
**Solution**: Upgrade Python or use `python3` command

#### 2. Missing Dependencies
\`\`\`
ModuleNotFoundError: No module named 'binance'
\`\`\`
**Solution**: 
\`\`\`bash
pip install -r requirements.txt
# or
pip install python-binance python-dotenv
\`\`\`

#### 3. API Key Issues
\`\`\`
Error: API credentials not found
\`\`\`
**Solutions**:
- Check `.env` file exists and has correct format
- Verify environment variables are set
- Ensure no extra spaces in API keys
- Confirm API key has Futures permissions

#### 4. Connection Issues
\`\`\`
Error: Failed to initialize bot
\`\`\`
**Solutions**:
- Check internet connection
- Verify API keys are correct
- Ensure testnet is accessible
- Check firewall settings

#### 5. Permission Errors
\`\`\`
PermissionError: [Errno 13] Permission denied: 'logs'
\`\`\`
**Solution**: 
\`\`\`bash
# Create logs directory manually
mkdir logs
chmod 755 logs
\`\`\`

### Debug Mode

For detailed troubleshooting, enable debug logging:

\`\`\`bash
export LOG_LEVEL=DEBUG
python main.py
\`\`\`

This will show detailed API requests, responses, and internal operations.

### Verification Checklist

Before running the bot, verify:

- [ ] Python 3.7+ installed
- [ ] All dependencies installed (`pip list | grep binance`)
- [ ] Binance Testnet account created
- [ ] API keys generated with Futures permissions
- [ ] `.env` file created with correct credentials
- [ ] `logs/` directory exists
- [ ] Configuration validates successfully
- [ ] Test connection works

## Next Steps

Once setup is complete:

1. **Read the main README.md** for usage instructions
2. **Start with small test trades** to familiarize yourself
3. **Monitor the logs** to understand bot behavior
4. **Customize configuration** as needed
5. **Explore advanced features** like stop-limit orders

## Getting Help

If you encounter issues:

1. **Check logs** in the `logs/` directory
2. **Review error messages** carefully
3. **Verify configuration** using the test commands
4. **Ensure API keys** have correct permissions
5. **Test with minimal configuration** first


---

 Run `python main.py` and begin with small test orders!
