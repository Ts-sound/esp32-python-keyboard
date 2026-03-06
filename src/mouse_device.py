"""
Mouse Device

Provides high-level mouse API, encapsulates HID driver.
"""

import time

from hid_driver import MouseDriver


class MouseDevice:
    """
    Mouse Device Class
    
    Provides high-level mouse API, supports:
    - Mouse button press/release
    - Mouse movement
    - Wheel scrolling
    """
    
    def __init__(self, device_name="ESP32-Mouse"):
        """
        Initialize mouse device
        
        Args:
            device_name: Device name
        """
        self._hid = MouseDriver(device_name)
        self._buttons = [0, 0, 0]
    
    def start(self):
        """
        Start mouse
        
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
    
    def click(self, button="left"):
        """
        Click mouse button
        
        Args:
            button: Button name ('left', 'middle', 'right')
        """
        try:
            if button == "left":
                idx = 0
            elif button == "middle":
                idx = 1
            elif button == "right":
                idx = 2
            else:
                print(f"[WARN] Unknown button: {button}")
                return
            
            self._buttons[idx] = 1
            self._hid.set_buttons(*self._buttons)
            time.sleep_ms(50)
            self._buttons[idx] = 0
            self._hid.set_buttons(*self._buttons)
        except Exception as e:
            print(f"[ERROR] MouseDevice.click: {e}")
            import sys
            sys.print_exception(e)
    
    def press(self, button="left"):
        """
        Press mouse button
        
        Args:
            button: Button name
        """
        try:
            if button == "left":
                idx = 0
            elif button == "middle":
                idx = 1
            elif button == "right":
                idx = 2
            else:
                print(f"[WARN] Unknown button: {button}")
                return
            
            self._buttons[idx] = 1
            self._hid.set_buttons(*self._buttons)
        except Exception as e:
            print(f"[ERROR] MouseDevice.press: {e}")
            import sys
            sys.print_exception(e)
    
    def release(self, button="left"):
        """
        Release mouse button
        
        Args:
            button: Button name
        """
        try:
            if button == "left":
                idx = 0
            elif button == "middle":
                idx = 1
            elif button == "right":
                idx = 2
            else:
                print(f"[WARN] Unknown button: {button}")
                return
            
            self._buttons[idx] = 0
            self._hid.set_buttons(*self._buttons)
        except Exception as e:
            print(f"[ERROR] MouseDevice.release: {e}")
            import sys
            sys.print_exception(e)
    
    def move(self, x=0, y=0):
        """
        Move mouse
        
        Args:
            x: X axis displacement (-127 to 127)
            y: Y axis displacement (-127 to 127)
        """
        try:
            self._hid.move(x=x, y=y)
        except Exception as e:
            print(f"[ERROR] MouseDevice.move: {e}")
            import sys
            sys.print_exception(e)
    
    def scroll(self, steps=1):
        """
        Scroll wheel
        
        Args:
            steps: Scroll steps (positive up, negative down)
        """
        try:
            self._hid.move(wheel=steps)
        except Exception as e:
            print(f"[ERROR] MouseDevice.scroll: {e}")
            import sys
            sys.print_exception(e)
    
    def is_connected(self):
        """
        Check connection status
        
        Returns:
            bool: Connection state
        """
        return self._hid.is_connected()
