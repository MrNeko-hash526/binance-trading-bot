#!/usr/bin/env python3
"""
Setup script for the Binance Futures Trading Bot.
This script helps users set up the bot with proper configuration.
"""

import os
import sys
import json
from pathlib import Path
from config import ConfigManager

def print_banner():
    """Print setup banner."""
    print("=" * 60)
    print("BINANCE FUTURES TRADING BOT SETUP")
    print("=" * 60)
    print("This script will help you set up the trading bot.")
    print()

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✓ Python version: {sys.version.split()[0]}")

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = ['binance', 'python-dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} is missing")
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    
    return True

def create_directories():
    """Create necessary directories."""
    directories = ['logs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")

def setup_configuration():
    """Set up configuration files."""
    config_manager = ConfigManager()
    
    # Create example files
    config_manager.create_example_files()
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("\n" + "-" * 40)
        print("API CREDENTIALS SETUP")
        print("-" * 40)
        
        setup_env = input("Do you want to set up API credentials now? (y/n): ").lower().strip()
        
        if setup_env in ['y', 'yes']:
            api_key = input("Enter your Binance API Key: ").strip()
            api_secret = input("Enter your Binance API Secret: ").strip()
            
            if api_key and api_secret:
                env_content = f"""# Binance API Configuration
BINANCE_API_KEY={api_key}
BINANCE_API_SECRET={api_secret}
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
                with open('.env', 'w') as f:
                    f.write(env_content)
                
                print("✓ .env file created with your credentials")
            else:
                print("⚠ Skipped credential setup - you'll need to set them manually")
        else:
            print("⚠ Skipped credential setup - you'll need to set them manually")
    else:
        print("✓ .env file already exists")

def test_configuration():
    """Test the configuration."""
    print("\n" + "-" * 40)
    print("CONFIGURATION TEST")
    print("-" * 40)
    
    try:
        config_manager = ConfigManager()
        
        # Test basic config loading
        print("✓ Configuration loaded successfully")
        
        # Test API credentials
        try:
            api_key, api_secret = config_manager.get_api_credentials()
            print("✓ API credentials found")
            
            # Don't actually test connection during setup
            print("⚠ API connection test skipped (run the bot to test)")
            
        except ValueError as e:
            print(f"✗ API credentials issue: {e}")
            return False
        
        # Test validation
        if config_manager.validate_config():
            print("✓ Configuration validation passed")
        else:
            print("✗ Configuration validation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def show_next_steps():
    """Show next steps to the user."""
    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)
    print("Next steps:")
    print("1. Make sure you have Binance Futures Testnet account:")
    print("   https://testnet.binancefuture.com")
    print()
    print("2. Run the trading bot:")
    print("   python main.py")
    print()
    print("3. Check the logs directory for trading logs")
    print()
    print("4. Customize config.json for advanced settings")
    print()
    print("Files created:")
    print("- .env (your API credentials)")
    print("- config.example.json (example configuration)")
    print("- logs/ (directory for log files)")
    print("=" * 60)

def main():
    """Main setup function."""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Check dependencies
    if not check_dependencies():
        print("\nPlease install missing dependencies and run setup again.")
        sys.exit(1)
    
    # Create directories
    print("\nCreating directories...")
    create_directories()
    
    # Setup configuration
    print("\nSetting up configuration...")
    setup_configuration()
    
    # Test configuration
    if test_configuration():
        show_next_steps()
    else:
        print("\n⚠ Setup completed with warnings. Please check your configuration.")
        print("You can run the bot with: python main.py")

if __name__ == "__main__":
    main()
