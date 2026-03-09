"""
Keyboard Application

Application layer logic, coordinates service layer modules.
"""

import asyncio
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
from keyboard_service import KeyboardService


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
        self._keyboard_service = None
        self._rf4_task = None
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
            
            # 5. Keyboard service (handles WiFi commands)
            self._keyboard_service = KeyboardService(
                keyboard_device=self._keyboard,
                msg_queue=self._msg_queue
            )
            print("[INFO] Keyboard service initialized")
            
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
    
    async def run_async(self):
        """Run main loop (async) - follows keyboard_example.py pattern"""
        # Start RF4 as background task
        self._rf4_task = asyncio.create_task(self._rf4.run_async())
        
        # Main WiFi loop
        while self._running:
            # Wait for client connection (async polling)
            if not self._wifi.has_client():
                if not await self._wifi.wait_for_client_async(WIFI_TIMEOUT_SEC):
                    continue
                print("[INFO] Client connected")
            
            # Process data (async polling)
            try:
                data = await self._wifi.recv_data_async()
                if data:
                    print(f"[RECV] {data}")
                elif data is None:
                    # Client disconnected
                    print("[INFO] Client disconnected, waiting for new connection...")
                    self._wifi.close_client()
                # data == "": no data, continue
                
            except OSError as e:
                print(f"[ERROR] Network error: {e}")
                self._wifi.close_client()
            
            # Commands handled by keyboard_service via message queue
            # RF4 runs in background task
            
            await asyncio.sleep_ms(MAIN_LOOP_INTERVAL_MS)
    
    async def stop_async(self):
        """Stop application (async)"""
        self._running = False
        
        # Cancel RF4 task
        if self._rf4_task:
            self._rf4_task.cancel()
            try:
                await self._rf4_task
            except asyncio.CancelledError:
                pass
        
        # Close WiFi
        if self._wifi:
            self._wifi.close()
        
        print("[INFO] Application stopped")
    
    def run(self):
        """Run main loop (blocking) - legacy support"""
        asyncio.run(self.run_async())
    
    def stop(self):
        """Stop application (blocking) - legacy support"""
        asyncio.run(self.stop_async())
    
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
