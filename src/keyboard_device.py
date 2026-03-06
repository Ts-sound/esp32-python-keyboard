"""
Keyboard Device

Provides high-level keyboard API, encapsulates HID driver.
Supports N-key rollover and string sending.
"""

import time

from hid_driver import HIDDriver
from hid_mapper import HID_KEYMAP


class KeyboardDevice:
    """
    Keyboard Device Class
    
    Provides high-level keyboard API, supports:
    - Single key press/release
    - N-key rollover (up to 6 keys)
    - String sending
    - Modifier key support
    """
    
    def __init__(self, device_name="ESP32-Keyboard"):
        """
        Initialize keyboard device
        
        Args:
            device_name: Device name
        """
        self._hid = HIDDriver(device_name)
        self._pressed_keys = []
    
    def start(self):
        """
        Start keyboard
        
        Returns:
            bool: Success status
        """
        return self._hid.start()
    
    def start_advertising(self):
        """
        Start advertising
        
        Returns:
            bool: Success status
        """
        return self._hid.start_advertising()
    
    def stop_advertising(self):
        """
        Stop advertising
        
        Returns:
            bool: Success status
        """
        return self._hid.stop_advertising()
    
    def press(self, key):
        """
        Press key
        
        Args:
            key: Key name (e.g., 'a', 'enter', 'F1')
            
        Returns:
            bool: Success status
        """
        try:
            if key not in HID_KEYMAP:
                print(f"[WARN] Unknown key: {key}")
                return False
            
            code = HID_KEYMAP[key]
            if code not in self._pressed_keys:
                self._pressed_keys.append(code)
            return self._send_report()
        except Exception as e:
            print(f"[ERROR] KeyboardDevice.press: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def release(self, key):
        """
        Release key
        
        Args:
            key: Key name
            
        Returns:
            bool: Success status
        """
        try:
            if key not in HID_KEYMAP:
                return False
            
            code = HID_KEYMAP[key]
            if code in self._pressed_keys:
                self._pressed_keys.remove(code)
            return self._send_report()
        except Exception as e:
            print(f"[ERROR] KeyboardDevice.release: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def release_all(self):
        """
        Release all keys
        
        Returns:
            bool: Success status
        """
        try:
            self._pressed_keys = []
            return self._hid.release_all()
        except Exception as e:
            print(f"[ERROR] KeyboardDevice.release_all: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def send_string(self, text):
        """
        Send string
        
        Args:
            text: String to send
            
        Returns:
            bool: Success status
        """
        try:
            for char in text:
                char_lower = char.lower()
                is_upper = char.isupper()
                
                if char_lower not in HID_KEYMAP:
                    print(f"[WARN] Unknown char: {char}")
                    continue
                
                code = HID_KEYMAP[char_lower]
                
                if is_upper:
                    self._hid.send_keys([code], {'left_shift': 1})
                else:
                    self._hid.send_keys([code])
                
                time.sleep_ms(20)
                self._hid.release_all()
                time.sleep_ms(20)
            
            return True
        except Exception as e:
            print(f"[ERROR] KeyboardDevice.send_string: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def set_modifiers(self, **kwargs):
        """
        Set modifiers
        
        Args:
            left_control, left_shift, left_alt, left_gui,
            right_control, right_shift, right_alt, right_gui
            
        Returns:
            bool: Success status
        """
        try:
            self._hid.send_keys(self._pressed_keys[:6], kwargs)
            return True
        except Exception as e:
            print(f"[ERROR] KeyboardDevice.set_modifiers: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def _send_report(self):
        """Send HID report"""
        return self._hid.send_keys(self._pressed_keys[:6])
    
    def is_connected(self):
        """
        Check connection status
        
        Returns:
            bool: Connection state
        """
        return self._hid.is_connected()
    
    def set_battery_level(self, level):
        """
        Set battery level
        
        Args:
            level: Battery percentage (0-100)
        """
        self._hid.set_battery_level(level)
    
    def notify_battery_level(self):
        """Notify battery level"""
        self._hid.notify_battery_level()
