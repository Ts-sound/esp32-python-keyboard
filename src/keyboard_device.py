"""
Keyboard Device

Provides high-level keyboard API using hid_services.Keyboard directly.
Supports N-key rollover and string sending.
"""

import time
import sys

from hid_services import Keyboard
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
        self._keyboard = Keyboard(device_name)
        self._pressed_keys = []
        self._modifiers = {}
        self._setup_callbacks()
    
    def _setup_callbacks(self):
        """Setup state change callback"""
        self._keyboard.set_state_change_callback(self._on_state_change)
    
    def _on_state_change(self):
        """State change callback"""
        state = self._keyboard.get_state()
        print(f"[INFO] Keyboard state changed: {state}")
    
    def start(self):
        """
        Start keyboard
        
        Returns:
            bool: Success status
        """
        try:
            # Wait for BLE hardware to be ready
            time.sleep_ms(500)
            self._keyboard.start()
            return True
        except OSError as e:
            if e.errno == 116:  # ETIMEDOUT
                print("[WARN] BLE init timeout, retrying...")
                time.sleep_ms(1000)
                try:
                    self._keyboard.start()
                    return True
                except Exception as e:
                    print(f"[ERROR] KeyboardDevice.start: {e}")
                    sys.print_exception(e)
                    return False
            print(f"[ERROR] KeyboardDevice.start: {e}")
            sys.print_exception(e)
            return False
        except Exception as e:
            print(f"[ERROR] KeyboardDevice.start: {e}")
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
            print(f"[ERROR] KeyboardDevice.start_advertising: {e}")
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
            print(f"[ERROR] KeyboardDevice.stop_advertising: {e}")
            sys.print_exception(e)
            return False
    
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
            self._modifiers = {}
            self._keyboard.set_keys()
            self._keyboard.set_modifiers()
            self._keyboard.notify_hid_report()
            return True
        except Exception as e:
            print(f"[ERROR] KeyboardDevice.release_all: {e}")
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
                    self._keyboard.set_keys(code)
                    self._keyboard.set_modifiers(left_shift=1)
                else:
                    self._keyboard.set_keys(code)
                    self._keyboard.set_modifiers()
                
                self._keyboard.notify_hid_report()
                time.sleep_ms(20)
                
                self._keyboard.set_keys()
                self._keyboard.set_modifiers()
                self._keyboard.notify_hid_report()
                time.sleep_ms(20)
            
            return True
        except Exception as e:
            print(f"[ERROR] KeyboardDevice.send_string: {e}")
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
            self._modifiers = kwargs
            self._keyboard.set_modifiers(**kwargs)
            self._keyboard.notify_hid_report()
            return True
        except Exception as e:
            print(f"[ERROR] KeyboardDevice.set_modifiers: {e}")
            sys.print_exception(e)
            return False
    
    def _send_report(self):
        """Send HID report"""
        try:
            # Clear and set keys (max 6)
            self._keyboard.set_keys(*self._pressed_keys[:6])
            
            # Apply modifiers
            if self._modifiers:
                self._keyboard.set_modifiers(**self._modifiers)
            else:
                self._keyboard.set_modifiers()
            
            self._keyboard.notify_hid_report()
            return True
        except Exception as e:
            print(f"[ERROR] KeyboardDevice._send_report: {e}")
            sys.print_exception(e)
            return False
    
    def is_connected(self):
        """
        Check connection status
        
        Returns:
            bool: Connection state
        """
        return self._keyboard.get_state() == Keyboard.DEVICE_CONNECTED
    
    def set_battery_level(self, level):
        """
        Set battery level
        
        Args:
            level: Battery percentage (0-100)
        """
        self._keyboard.set_battery_level(level)
    
    def notify_battery_level(self):
        """Notify battery level"""
        self._keyboard.notify_battery_level()
