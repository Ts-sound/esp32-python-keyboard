"""
Keyboard Application

Application layer logic, coordinates service layer modules.
"""

import time

from config import (
    HID_ADVERTISING_TIMEOUT_SEC,
    MAIN_LOOP_INTERVAL_MS,
    WIFI_TIMEOUT_SEC,
)
from keyboard_device import KeyboardDevice
from rf4_service import RF4Service
from wifi_service import WiFiService
from msg_queue import MessageQueue


class KeyboardApp:
    """
    Keyboard Application Class
    
    Coordinates all services and devices, provides unified application entry point.
    """
    
    def __init__(self):
        """Initialize application"""
        self._msg_queue = None
        self._keyboard = None
        self._wifi = None
        self._rf4 = None
        self._running = False
    
    def init(self):
        """
        Initialize all components
        
        Returns:
            bool: Success status
        """
        print("[INFO] Initializing components...")
        
        try:
            # 1. Message queue
            self._msg_queue = MessageQueue(max_size=10)
            print("[INFO] MessageQueue initialized")
            
            # 2. Keyboard device
            self._keyboard = KeyboardDevice()
            if not self._keyboard.start():
                print("[ERROR] Failed to start keyboard")
                return False
            print("[INFO] Keyboard started")
            
            # 3. WiFi service
            self._wifi = WiFiService(msg_queue=self._msg_queue)
            if not self._wifi.start():
                print("[ERROR] Failed to start WiFi")
                return False
            print("[INFO] WiFi started")
            
            # 4. RF4 service
            self._rf4 = RF4Service(
                keyboard_device=self._keyboard,
                msg_queue=self._msg_queue
            )
            print("[INFO] RF4 service initialized")
            
            return True
        except Exception as e:
            print(f"[ERROR] KeyboardApp.init: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def start(self):
        """
        Start application main loop
        
        Returns:
            bool: Success status
        """
        if not self.init():
            return False
        
        self._running = True
        
        # Start keyboard advertising
        self._keyboard.start_advertising()
        print("[INFO] Keyboard advertising started")
        
        # Start WiFi connection
        if self._wifi.connect():
            if self._wifi.start_server():
                print("[INFO] WiFi server ready")
        
        print("[INFO] Application started")
        return True
    
    def run(self):
        """Run main loop (blocking - wait for client, then process data)"""
        try:
            while self._running:
                # Wait for client connection (blocking with timeout)
                if not self._wifi.has_client():
                    if not self._wifi.wait_for_client(WIFI_TIMEOUT_SEC):
                        continue  # Timeout, check running state
                    print("[INFO] Starting data processing...")
                
                # Client connected, process data (blocking)
                try:
                    data = self._wifi.recv_data()
                    if data:
                        print(f"[RECV] {data}")
                    elif data is None:
                        # Client disconnected
                        print("[INFO] Client disconnected, waiting for new connection...")
                        self._wifi.close_client()
                except OSError as e:
                    # Network error - client disconnected
                    print(f"[ERROR] Network error: {e}")
                    self._wifi.close_client()
                
                # RF4 state check via message queue (non-blocking)
                # RF4 service has its own internal loop
                
                time.sleep_ms(MAIN_LOOP_INTERVAL_MS)
        except KeyboardInterrupt:
            print("[INFO] Stopping...")
        except Exception as e:
            print(f"[ERROR] KeyboardApp.run: {e}")
            import sys
            sys.print_exception(e)
        finally:
            self.stop()
    
    def stop(self):
        """Stop application"""
        print("[INFO] Stopping application...")
        self._running = False
        
        if self._wifi:
            self._wifi.close()
        
        print("[INFO] Application stopped")
    
    def get_keyboard(self):
        """Get keyboard device"""
        return self._keyboard
    
    def get_wifi(self):
        """Get WiFi service"""
        return self._wifi
    
    def get_rf4(self):
        """Get RF4 service"""
        return self._rf4
    
    def get_msg_queue(self):
        """Get message queue"""
        return self._msg_queue
