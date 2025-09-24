import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from typing import Dict, Any, Optional
import json
from datetime import datetime
from logger import log_trade, log_error, log_api_request, log_system_event

class BasicBot:
    """
    A simplified Binance Futures Testnet trading bot that supports market and limit orders.
    """
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """
        Initialize the trading bot with API credentials.
        
        Args:
            api_key (str): Binance API key
            api_secret (str): Binance API secret
            testnet (bool): Whether to use testnet (default: True)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        
        # Initialize Binance client
        try:
            self.client = Client(
                api_key=api_key,
                api_secret=api_secret,
                testnet=testnet
            )
            log_system_event("Bot initialized", {
                "testnet": testnet,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            log_error(e, "Bot initialization")
            raise
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get futures account information."""
        try:
            log_api_request("futures_account", {}, "REQUEST_SENT")
            
            account_info = self.client.futures_account()
            
            log_api_request("futures_account", {}, "SUCCESS")
            log_system_event("Account info retrieved", {
                "balance": account_info.get('totalWalletBalance', 'N/A')
            })
            
            return account_info
        except BinanceAPIException as e:
            log_api_request("futures_account", {}, f"API_ERROR: {e}")
            log_error(e, "get_account_info")
            raise
        except Exception as e:
            log_error(e, "get_account_info")
            raise
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
        """
        Place a market order.
        
        Args:
            symbol (str): Trading pair (e.g., 'BTCUSDT')
            side (str): 'BUY' or 'SELL'
            quantity (float): Order quantity
            
        Returns:
            Dict containing order details
        """
        try:
            order_params = {
                "symbol": symbol,
                "side": side,
                "type": "MARKET",
                "quantity": quantity
            }
            
            log_api_request("futures_create_order", order_params, "REQUEST_SENT")
            log_system_event("Placing market order", order_params)
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            
            # Format response
            order_details = {
                'orderId': order['orderId'],
                'symbol': order['symbol'],
                'side': order['side'],
                'type': order['type'],
                'quantity': order['origQty'],
                'status': order['status'],
                'timestamp': datetime.now().isoformat()
            }
            
            log_api_request("futures_create_order", order_params, "SUCCESS")
            log_trade(order_details, "MARKET_ORDER")
            log_system_event("Market order completed", order_details)
            
            return order_details
            
        except BinanceOrderException as e:
            log_api_request("futures_create_order", order_params, f"ORDER_ERROR: {e}")
            log_error(e, "place_market_order")
            raise
        except BinanceAPIException as e:
            log_api_request("futures_create_order", order_params, f"API_ERROR: {e}")
            log_error(e, "place_market_order")
            raise
        except Exception as e:
            log_error(e, "place_market_order")
            raise
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> Dict[str, Any]:
        """
        Place a limit order.
        
        Args:
            symbol (str): Trading pair (e.g., 'BTCUSDT')
            side (str): 'BUY' or 'SELL'
            quantity (float): Order quantity
            price (float): Order price
            
        Returns:
            Dict containing order details
        """
        try:
            order_params = {
                "symbol": symbol,
                "side": side,
                "type": "LIMIT",
                "quantity": quantity,
                "price": price
            }
            
            log_api_request("futures_create_order", order_params, "REQUEST_SENT")
            log_system_event("Placing limit order", order_params)
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                timeInForce='GTC',  # Good Till Cancelled
                quantity=quantity,
                price=price
            )
            
            # Format response
            order_details = {
                'orderId': order['orderId'],
                'symbol': order['symbol'],
                'side': order['side'],
                'type': order['type'],
                'quantity': order['origQty'],
                'price': order['price'],
                'status': order['status'],
                'timestamp': datetime.now().isoformat()
            }
            
            log_api_request("futures_create_order", order_params, "SUCCESS")
            log_trade(order_details, "LIMIT_ORDER")
            log_system_event("Limit order completed", order_details)
            
            return order_details
            
        except BinanceOrderException as e:
            log_api_request("futures_create_order", order_params, f"ORDER_ERROR: {e}")
            log_error(e, "place_limit_order")
            raise
        except BinanceAPIException as e:
            log_api_request("futures_create_order", order_params, f"API_ERROR: {e}")
            log_error(e, "place_limit_order")
            raise
        except Exception as e:
            log_error(e, "place_limit_order")
            raise
    
    def place_stop_limit_order(self, symbol: str, side: str, quantity: float, 
                              price: float, stop_price: float) -> Dict[str, Any]:
        """
        Place a stop-limit order (bonus feature).
        
        Args:
            symbol (str): Trading pair (e.g., 'BTCUSDT')
            side (str): 'BUY' or 'SELL'
            quantity (float): Order quantity
            price (float): Limit price
            stop_price (float): Stop price
            
        Returns:
            Dict containing order details
        """
        try:
            order_params = {
                "symbol": symbol,
                "side": side,
                "type": "STOP",
                "quantity": quantity,
                "price": price,
                "stopPrice": stop_price
            }
            
            log_api_request("futures_create_order", order_params, "REQUEST_SENT")
            log_system_event("Placing stop-limit order", order_params)
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP',
                timeInForce='GTC',
                quantity=quantity,
                price=price,
                stopPrice=stop_price
            )
            
            # Format response
            order_details = {
                'orderId': order['orderId'],
                'symbol': order['symbol'],
                'side': order['side'],
                'type': order['type'],
                'quantity': order['origQty'],
                'price': order['price'],
                'stopPrice': order['stopPrice'],
                'status': order['status'],
                'timestamp': datetime.now().isoformat()
            }
            
            log_api_request("futures_create_order", order_params, "SUCCESS")
            log_trade(order_details, "STOP_LIMIT_ORDER")
            log_system_event("Stop-limit order completed", order_details)
            
            return order_details
            
        except BinanceOrderException as e:
            log_api_request("futures_create_order", order_params, f"ORDER_ERROR: {e}")
            log_error(e, "place_stop_limit_order")
            raise
        except BinanceAPIException as e:
            log_api_request("futures_create_order", order_params, f"API_ERROR: {e}")
            log_error(e, "place_stop_limit_order")
            raise
        except Exception as e:
            log_error(e, "place_stop_limit_order")
            raise
    
    def get_symbol_info(self, symbol: str) -> Dict[str, Any]:
        """Get symbol information for validation."""
        try:
            exchange_info = self.client.futures_exchange_info()
            for s in exchange_info['symbols']:
                if s['symbol'] == symbol:
                    return s
            return None
        except Exception as e:
            log_error(e, "get_symbol_info")
            return None
    
    def validate_order_params(self, symbol: str, quantity: float, price: Optional[float] = None) -> bool:
        """
        Validate order parameters.
        
        Args:
            symbol (str): Trading pair
            quantity (float): Order quantity
            price (float, optional): Order price for limit orders
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Check if symbol exists
            symbol_info = self.get_symbol_info(symbol)
            if not symbol_info:
                log_error(f"Invalid symbol: {symbol}", "validate_order_params")
                return False
            
            # Check quantity
            if quantity <= 0:
                log_error(f"Invalid quantity: {quantity}", "validate_order_params")
                return False
            
            # Check price if provided
            if price is not None and price <= 0:
                log_error(f"Invalid price: {price}", "validate_order_params")
                return False
            
            return True
            
        except Exception as e:
            log_error(e, "validate_order_params")
            return False
