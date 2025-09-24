import sys
import logging
from typing import Optional
from bot import BasicBot
from config import ConfigManager
from logger import setup_logging, log_system_event, log_error, get_logger_instance
from utils import (
    validate_input, validate_trading_pair, 
    validate_order_side, validate_order_type, print_order_summary
)

class TradingBotCLI:
    """
    Command Line Interface for the Binance Futures Trading Bot.
    """
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.bot: Optional[BasicBot] = None
        self.setup()
    
    def setup(self):
        """Initialize the CLI and bot."""
        log_config = {
            'log_level': self.config_manager.get('log_level', 'INFO'),
            'max_bytes': self.config_manager.get('max_log_size', 10 * 1024 * 1024),
            'backup_count': self.config_manager.get('log_backup_count', 5)
        }
        setup_logging(log_config)
        
        log_system_event("CLI startup", {"config": log_config})
        
        # Validate configuration
        if not self.config_manager.validate_config():
            print("Configuration validation failed. Please check your API credentials.")
            self.show_setup_instructions()
            sys.exit(1)
        
        # Initialize bot
        try:
            api_key, api_secret = self.config_manager.get_api_credentials()
            testnet = self.config_manager.is_testnet()
            
            self.bot = BasicBot(api_key, api_secret, testnet)
            
            # Test connection
            account_info = self.bot.get_account_info()
            print(f"Connected to Binance {'Testnet' if testnet else 'Live'} successfully!")
            print(f"Account Balance: {account_info.get('totalWalletBalance', 'N/A')} USDT")
            
            log_system_event("Bot connection established", {
                "testnet": testnet,
                "balance": account_info.get('totalWalletBalance', 'N/A')
            })
            
        except Exception as e:
            log_error(e, "CLI setup")
            print(f"Error: {e}")
            sys.exit(1)
    
    def show_setup_instructions(self):
        """Show setup instructions for API credentials."""
        print("\n" + "="*60)
        print("SETUP INSTRUCTIONS")
        print("="*60)
        print("1. Get your API credentials from Binance Futures Testnet:")
        print("   https://testnet.binancefuture.com")
        print("\n2. Set environment variables:")
        print("   export BINANCE_API_KEY='your_api_key_here'")
        print("   export BINANCE_API_SECRET='your_api_secret_here'")
        print("\n3. Or create a .env file with:")
        print("   BINANCE_API_KEY=your_api_key_here")
        print("   BINANCE_API_SECRET=your_api_secret_here")
        print("="*60)
    
    def show_main_menu(self):
        """Display the main menu."""
        print("\n" + "="*50)
        print("BINANCE FUTURES TRADING BOT")
        print("="*50)
        print("1. Place Market Order")
        print("2. Place Limit Order")
        print("3. Place Stop-Limit Order (Advanced)")
        print("4. View Account Info")
        print("5. Exit")
        print("="*50)
    
    def get_order_inputs(self, order_type: str) -> dict:
        """
        Get order inputs from user.
        
        Args:
            order_type (str): Type of order ('MARKET', 'LIMIT', 'STOP-LIMIT')
            
        Returns:
            dict: Order parameters
        """
        print(f"\n--- {order_type} ORDER ---")
        
        # Get trading pair
        default_symbol = self.config_manager.get_default_symbol()
        symbol_input = input(f"Enter trading pair (default: {default_symbol}): ").strip()
        symbol = validate_trading_pair(symbol_input if symbol_input else default_symbol)
        
        # Get order side
        while True:
            try:
                side_input = input("Enter order side (BUY/SELL): ").strip()
                side = validate_order_side(side_input)
                break
            except ValueError as e:
                print(f"Error: {e}")
        
        # Get quantity
        quantity = validate_input(
            "Enter quantity: ",
            float,
            min_value=0.001
        )
        
        order_params = {
            'symbol': symbol,
            'side': side,
            'quantity': quantity
        }
        
        # Get price for limit orders
        if order_type in ['LIMIT', 'STOP-LIMIT']:
            price = validate_input(
                "Enter limit price: ",
                float,
                min_value=0.01
            )
            order_params['price'] = price
        
        # Get stop price for stop-limit orders
        if order_type == 'STOP-LIMIT':
            stop_price = validate_input(
                "Enter stop price: ",
                float,
                min_value=0.01
            )
            order_params['stop_price'] = stop_price
        
        return order_params
    
    def confirm_order(self, order_params: dict, order_type: str) -> bool:
        """
        Show order confirmation and get user approval.
        
        Args:
            order_params (dict): Order parameters
            order_type (str): Order type
            
        Returns:
            bool: True if confirmed, False otherwise
        """
        print("\n" + "-"*40)
        print("ORDER CONFIRMATION")
        print("-"*40)
        print(f"Type: {order_type}")
        print(f"Symbol: {order_params['symbol']}")
        print(f"Side: {order_params['side']}")
        print(f"Quantity: {order_params['quantity']}")
        
        if 'price' in order_params:
            print(f"Price: {order_params['price']}")
        
        if 'stop_price' in order_params:
            print(f"Stop Price: {order_params['stop_price']}")
        
        print("-"*40)
        
        while True:
            confirm = input("Confirm order? (y/n): ").strip().lower()
            if confirm in ['y', 'yes']:
                return True
            elif confirm in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' or 'n'")
    
    def place_market_order(self):
        """Handle market order placement."""
        try:
            log_system_event("User initiated market order")
            
            order_params = self.get_order_inputs('MARKET')
            
            if not self.confirm_order(order_params, 'MARKET'):
                print("Order cancelled.")
                log_system_event("Market order cancelled by user")
                return
            
            # Validate parameters
            if not self.bot.validate_order_params(
                order_params['symbol'], 
                order_params['quantity']
            ):
                print("Invalid order parameters.")
                log_system_event("Market order failed validation", order_params)
                return
            
            # Place order
            print("\nPlacing market order...")
            order_result = self.bot.place_market_order(
                order_params['symbol'],
                order_params['side'],
                order_params['quantity']
            )
            
            print_order_summary(order_result)
            
        except Exception as e:
            log_error(e, "CLI place_market_order")
            print(f"Error: {e}")
    
    def place_limit_order(self):
        """Handle limit order placement."""
        try:
            order_params = self.get_order_inputs('LIMIT')
            
            if not self.confirm_order(order_params, 'LIMIT'):
                print("Order cancelled.")
                return
            
            # Validate parameters
            if not self.bot.validate_order_params(
                order_params['symbol'], 
                order_params['quantity'],
                order_params['price']
            ):
                print("Invalid order parameters.")
                return
            
            # Place order
            print("\nPlacing limit order...")
            order_result = self.bot.place_limit_order(
                order_params['symbol'],
                order_params['side'],
                order_params['quantity'],
                order_params['price']
            )
            
            print_order_summary(order_result)
            
        except Exception as e:
            log_error(e, "CLI place_limit_order")
            print(f"Error: {e}")
    
    def place_stop_limit_order(self):
        """Handle stop-limit order placement."""
        try:
            order_params = self.get_order_inputs('STOP-LIMIT')
            
            if not self.confirm_order(order_params, 'STOP-LIMIT'):
                print("Order cancelled.")
                return
            
            # Validate parameters
            if not self.bot.validate_order_params(
                order_params['symbol'], 
                order_params['quantity'],
                order_params['price']
            ):
                print("Invalid order parameters.")
                return
            
            # Place order
            print("\nPlacing stop-limit order...")
            order_result = self.bot.place_stop_limit_order(
                order_params['symbol'],
                order_params['side'],
                order_params['quantity'],
                order_params['price'],
                order_params['stop_price']
            )
            
            print_order_summary(order_result)
            
        except Exception as e:
            log_error(e, "CLI place_stop_limit_order")
            print(f"Error: {e}")
    
    def show_account_info(self):
        """Display account information."""
        try:
            print("\nFetching account information...")
            account_info = self.bot.get_account_info()
            
            print("\n" + "="*50)
            print("ACCOUNT INFORMATION")
            print("="*50)
            print(f"Total Wallet Balance: {account_info.get('totalWalletBalance', 'N/A')} USDT")
            print(f"Total Unrealized PnL: {account_info.get('totalUnrealizedProfit', 'N/A')} USDT")
            print(f"Total Margin Balance: {account_info.get('totalMarginBalance', 'N/A')} USDT")
            print(f"Available Balance: {account_info.get('availableBalance', 'N/A')} USDT")
            
            # Show positions if any
            positions = [pos for pos in account_info.get('positions', []) 
                        if float(pos.get('positionAmt', 0)) != 0]
            
            if positions:
                print("\nOpen Positions:")
                print("-" * 30)
                for pos in positions:
                    print(f"Symbol: {pos.get('symbol', 'N/A')}")
                    print(f"Size: {pos.get('positionAmt', 'N/A')}")
                    print(f"Entry Price: {pos.get('entryPrice', 'N/A')}")
                    print(f"PnL: {pos.get('unRealizedProfit', 'N/A')}")
                    print("-" * 30)
            else:
                print("\nNo open positions.")
            
            print("="*50)
            
        except Exception as e:
            log_error(e, "CLI show_account_info")
            print(f"Error: {e}")
    
    def run(self):
        """Run the CLI main loop."""
        print("Welcome to the Binance Futures Trading Bot!")
        log_system_event("CLI main loop started")
        
        while True:
            try:
                self.show_main_menu()
                
                choice = input("\nSelect an option (1-5): ").strip()
                log_system_event("User menu selection", {"choice": choice})
                
                if choice == '1':
                    self.place_market_order()
                elif choice == '2':
                    self.place_limit_order()
                elif choice == '3':
                    self.place_stop_limit_order()
                elif choice == '4':
                    self.show_account_info()
                elif choice == '5':
                    print("Thank you for using the trading bot. Goodbye!")
                    log_system_event("CLI shutdown by user")
                    break
                else:
                    print("Invalid option. Please select 1-5.")
                    log_system_event("Invalid menu selection", {"choice": choice})
                
                # Pause before showing menu again
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user. Goodbye!")
                log_system_event("CLI interrupted by user")
                break
            except Exception as e:
                log_error(e, "CLI main loop")
                print(f"Unexpected error: {e}")
                input("Press Enter to continue...")

def main():
    """Main entry point for the CLI."""
    try:
        cli = TradingBotCLI()
        cli.run()
    except Exception as e:
        log_error(e, "CLI main")
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
