"""
WiFi Service

Encapsulates ESP32 WiFi functionality, provides TCP server and client communication.
Supports auto-reconnect and message queue integration.
"""

import network
import socket
import time

from config import (
    WIFI_SSID,
    WIFI_PASSWORD,
    WIFI_PORT,
    WIFI_TIMEOUT_SEC,
    WIFI_SOCKET_TIMEOUT_SEC,
)


class WiFiService:
    """
    WiFi Service Class
    
    Provides:
    - WiFi connection management
    - TCP server
    - Client communication
    - Message queue integration
    """
    
    def __init__(self, msg_queue=None):
        """
        Initialize WiFi service
        
        Args:
            msg_queue: Message queue instance
        """
        self._wlan = network.WLAN(network.STA_IF)
        self._socket = None
        self._client = None
        self._msg_queue = msg_queue
        self._connected = False
    
    def start(self):
        """
        Start WiFi
        
        Returns:
            bool: Success status
        """
        try:
            self._wlan.active(True)
            print("[INFO] WiFi activated")
            return True
        except Exception as e:
            print(f"[ERROR] WiFiService.start: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def connect(self):
        """
        Connect to WiFi
        
        Returns:
            bool: Connection success status
        """
        try:
            print(f"[INFO] Connecting to {WIFI_SSID}...")
            self._wlan.connect(WIFI_SSID, WIFI_PASSWORD)
            
            timeout = time.time() + WIFI_TIMEOUT_SEC
            while time.time() < timeout:
                if self._wlan.isconnected():
                    self._connected = True
                    print(f"[INFO] Connected: {self._wlan.ifconfig()}")
                    return True
                time.sleep(1)
            
            print("[ERROR] WiFi connection timeout")
            return False
        except Exception as e:
            print(f"[ERROR] WiFiService.connect: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def reconnect(self):
        """
        Reconnect WiFi
        
        Returns:
            bool: Success status
        """
        try:
            if self._wlan.isconnected():
                self._wlan.disconnect()
            time.sleep(1)
            return self.connect()
        except Exception as e:
            print(f"[ERROR] WiFiService.reconnect: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def start_server(self):
        """
        Start TCP server
        
        Returns:
            bool: Success status
        """
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.bind(('0.0.0.0', WIFI_PORT))
            self._socket.listen(5)
            print(f"[INFO] Server listening on port {WIFI_PORT}")
            return True
        except Exception as e:
            print(f"[ERROR] WiFiService.start_server: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def has_client(self):
        """
        Check if a client is connected
        
        Returns:
            bool: Client connection state
        """
        return self._client is not None
    
    def wait_for_client(self, timeout=None):
        """
        Wait for client connection (blocking with timeout)
        
        Args:
            timeout: Timeout in seconds (None for infinite)
            
        Returns:
            bool: Success status
        """
        try:
            if self._socket:
                self._socket.settimeout(timeout)
                self._client, addr = self._socket.accept()
                self._client.settimeout(WIFI_SOCKET_TIMEOUT_SEC)
                print(f"[INFO] Client connected: {addr}")
                return True
            return False
        except OSError as e:
            if e.errno == 110:  # ETIMEDOUT
                return False
            print(f"[ERROR] WiFiService.wait_for_client: {e}")
            import sys
            sys.print_exception(e)
            return False
        except Exception as e:
            print(f"[ERROR] WiFiService.wait_for_client: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def close_client(self):
        """Close current client connection"""
        try:
            if self._client:
                self._client.close()
                self._client = None
                print("[INFO] Client disconnected")
        except Exception as e:
            print(f"[ERROR] WiFiService.close_client: {e}")
            import sys
            sys.print_exception(e)
    
    def accept_client(self):
        """
        Accept client connection (blocking)
        
        Returns:
            bool: Success status
        """
        try:
            if self._socket:
                self._client, addr = self._socket.accept()
                self._client.settimeout(WIFI_SOCKET_TIMEOUT_SEC)
                print(f"[INFO] Client connected: {addr}")
                return True
            return False
        except Exception as e:
            print(f"[ERROR] WiFiService.accept_client: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def recv_data(self, buffer_size=1024):
        """
        Receive data (blocking with short timeout)
        
        Args:
            buffer_size: Buffer size
            
        Returns:
            str: Received data, or None if client disconnected
        """
        try:
            if self._client:
                self._client.settimeout(1.0)  # Short timeout for responsive disconnect detection
                data = self._client.recv(buffer_size)
                if data:
                    msg = data.decode('utf-8')
                    if self._msg_queue:
                        self._msg_queue.publish("wifi/raw", msg)
                    return msg
                else:
                    # Empty data means client disconnected
                    return None
            return None
        except OSError as e:
            if e.errno == 110:  # ETIMEDOUT - no data available
                return ""  # Empty string, client still connected
            print(f"[ERROR] WiFiService.recv_data: {e}")
            import sys
            sys.print_exception(e)
            return None
        except Exception as e:
            print(f"[ERROR] WiFiService.recv_data: {e}")
            import sys
            sys.print_exception(e)
            return None
    
    def send_data(self, data):
        """
        Send data
        
        Args:
            data: Data to send
            
        Returns:
            bool: Success status
        """
        try:
            if self._client:
                self._client.send(data.encode('utf-8'))
                return True
            return False
        except Exception as e:
            print(f"[ERROR] WiFiService.send_data: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def is_connected(self):
        """
        Check connection status
        
        Returns:
            bool: Connection state
        """
        return self._wlan.isconnected() and self._connected
    
    def get_ip(self):
        """
        Get IP address
        
        Returns:
            tuple: (ip, netmask, gateway, dns) or None
        """
        try:
            if self._wlan.isconnected():
                return self._wlan.ifconfig()
            return None
        except Exception as e:
            print(f"[ERROR] WiFiService.get_ip: {e}")
            import sys
            sys.print_exception(e)
            return None
    
    def close(self):
        """Close connection"""
        try:
            if self._client:
                self._client.close()
                self._client = None
            if self._socket:
                self._socket.close()
                self._socket = None
            print("[INFO] WiFi connection closed")
        except Exception as e:
            print(f"[ERROR] WiFiService.close: {e}")
            import sys
            sys.print_exception(e)
