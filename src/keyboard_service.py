"""
Keyboard Service

Handles WiFi commands to keyboard input conversion.
Subscribes to wifi/raw message queue.
"""

import time


class KeyboardService:
    """
    Keyboard Service Class
    
    Receives commands from WiFi and converts to keyboard actions.
    """
    
    def __init__(self, keyboard_device, msg_queue):
        """
        Initialize keyboard service
        
        Args:
            keyboard_device: KeyboardDevice instance
            msg_queue: MessageQueue instance
        """
        self._keyboard = keyboard_device
        
        # Subscribe to wifi/raw
        msg_queue.subscribe("wifi/raw", self._handle_command)
    
    def _handle_command(self, msg):
        """
        Handle WiFi command
        
        Command Format:
        - shift: Enable shift modifier
        - ctrl: Enable ctrl modifier
        - clear: Clear all keys and modifiers
        - <key>: Press key (e.g., "a", "enter", ";")
        
        Args:
            msg: Command string
        """
        try:
            if msg == "shift":
                self._keyboard.set_modifiers(left_shift=1)
            elif msg == "ctrl":
                self._keyboard.set_modifiers(left_control=1)
            elif msg == "clear":
                self._keyboard.release_all()
            else:
                # Press key
                self._keyboard.press(msg)
                time.sleep_ms(20)
                self._keyboard.release(msg)
        except Exception as e:
            print(f"[ERROR] KeyboardService._handle_command: {e}")
            import sys
            sys.print_exception(e)
