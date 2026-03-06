"""
HID Driver Wrapper

Encapsulates the hid_services module from MicroPythonBLEHID library.
Provides unified error handling and status checking.
"""

import sys

from hid_services import Keyboard as HIDKeyboard
from hid_services import Mouse as HIDMouse


class HIDDriver:
    """
    HID Driver Wrapper Class
    
    Encapsulates BLE HID Keyboard service with simplified API.
    """
    
    def __init__(self, device_name="ESP32-Keyboard"):
        """
        Initialize HID driver
        
        Args:
            device_name: Device name
        """
        self._keyboard = HIDKeyboard(device_name)
        self._connected = False
        self._setup_callbacks()
    
    def _setup_callbacks(self):
        """Setup callbacks"""
        self._keyboard.set_state_change_callback(self._on_state_change)
    
    def _on_state_change(self):
        """State change callback"""
        state = self._keyboard.get_state()
        print(f"[INFO] HID state changed: {state}")
    
    def start(self):
        """
        Start HID service
        
        Returns:
            bool: Success status
        """
        try:
            self._keyboard.start()
            return True
        except Exception as e:
            print(f"[ERROR] HIDDriver.start: {e}")
            sys.print_exception(e)
            return False
    
    def start_advertising(self):
        """
        Start advertising
        
        Returns:
            bool: Success status
        """
        try:
            self._keyboard.start_advertising()
            return True
        except Exception as e:
            print(f"[ERROR] HIDDriver.start_advertising: {e}")
            sys.print_exception(e)
            return False
    
    def stop_advertising(self):
        """
        Stop advertising
        
        Returns:
            bool: Success status
        """
        try:
            self._keyboard.stop_advertising()
            return True
        except Exception as e:
            print(f"[ERROR] HIDDriver.stop_advertising: {e}")
            sys.print_exception(e)
            return False
    
    def send_keys(self, keys=None, modifiers=None):
        """
        Send keys
        
        Args:
            keys: List of key codes (max 6)
            modifiers: Modifier dictionary
            
        Returns:
            bool: Success status
        """
        try:
            self._keyboard.set_keys()
            self._keyboard.set_modifiers()
            
            if keys and len(keys) > 0:
                self._keyboard.set_keys(*keys[:6])
            if modifiers:
                self._keyboard.set_modifiers(**modifiers)
            
            self._keyboard.notify_hid_report()
            return True
        except Exception as e:
            print(f"[ERROR] HIDDriver.send_keys: {e}")
            sys.print_exception(e)
            return False
    
    def release_all(self):
        """
        Release all keys
        
        Returns:
            bool: Success status
        """
        try:
            self._keyboard.set_keys()
            self._keyboard.set_modifiers()
            self._keyboard.notify_hid_report()
            return True
        except Exception as e:
            print(f"[ERROR] HIDDriver.release_all: {e}")
            sys.print_exception(e)
            return False
    
    def set_battery_level(self, level):
        """
        Set battery level
        
        Args:
            level: Battery percentage (0-100)
        """
        try:
            self._keyboard.set_battery_level(level)
        except Exception as e:
            print(f"[ERROR] HIDDriver.set_battery_level: {e}")
            sys.print_exception(e)
    
    def notify_battery_level(self):
        """Notify battery level"""
        try:
            self._keyboard.notify_battery_level()
        except Exception as e:
            print(f"[ERROR] HIDDriver.notify_battery_level: {e}")
            sys.print_exception(e)
    
    def is_connected(self):
        """
        Check connection status
        
        Returns:
            bool: Connection state
        """
        return self._keyboard.get_state() == HIDKeyboard.DEVICE_CONNECTED


class MouseDriver:
    """
    HID Mouse Driver Wrapper Class
    """
    
    def __init__(self, device_name="ESP32-Mouse"):
        """
        Initialize mouse driver
        
        Args:
            device_name: Device name
        """
        self._mouse = HIDMouse(device_name)
        self._setup_callbacks()
    
    def _setup_callbacks(self):
        """Setup callbacks"""
        self._mouse.set_state_change_callback(self._on_state_change)
    
    def _on_state_change(self):
        """State change callback"""
        print(f"[INFO] Mouse state changed: {self._mouse.get_state()}")
    
    def start(self):
        """Start mouse service"""
        try:
            self._mouse.start()
            return True
        except Exception as e:
            print(f"[ERROR] MouseDriver.start: {e}")
            sys.print_exception(e)
            return False
    
    def start_advertising(self):
        """Start advertising"""
        try:
            self._mouse.start_advertising()
            return True
        except Exception as e:
            print(f"[ERROR] MouseDriver.start_advertising: {e}")
            sys.print_exception(e)
            return False
    
    def set_buttons(self, b1=0, b2=0, b3=0):
        """
        Set mouse buttons
        
        Args:
            b1: Left button (0/1)
            b2: Middle button (0/1)
            b3: Right button (0/1)
        """
        try:
            self._mouse.set_buttons(b1, b2, b3)
            self._mouse.notify_hid_report()
        except Exception as e:
            print(f"[ERROR] MouseDriver.set_buttons: {e}")
            sys.print_exception(e)
    
    def move(self, x=0, y=0, wheel=0):
        """
        Move mouse
        
        Args:
            x: X axis displacement (-127 to 127)
            y: Y axis displacement (-127 to 127)
            wheel: Wheel displacement (-127 to 127)
        """
        try:
            self._mouse.move(x, y, wheel)
            self._mouse.notify_hid_report()
        except Exception as e:
            print(f"[ERROR] MouseDriver.move: {e}")
            sys.print_exception(e)
    
    def is_connected(self):
        """Check connection status"""
        return self._mouse.get_state() == HIDMouse.DEVICE_CONNECTED
