"""
RF4 Service

Implements RF4 auto-press functionality, supports JIG and PULL modes.
Receives control commands via message queue.
"""

import time
import random

from config import (
    RF4_JIG_PRESS_MS,
    RF4_JIG_RELEASE_MS,
    RF4_PULL_PRESS_MS,
    RF4_PULL_RELEASE_MS,
    RF4_RANDOM_VARIANCE,
)


class RF4State:
    """RF4 State Enum"""
    IDLE = 0
    JIG = 1
    PULL = 2


class RF4Service:
    """
    RF4 Service Class
    
    Provides:
    - JIG mode: Auto-press semicolon key
    - PULL mode: Auto-press semicolon and single quote keys
    - Message queue control interface
    - Random delay for anti-detection
    """
    
    def __init__(self, keyboard_device, msg_queue=None):
        """
        Initialize RF4 service
        
        Args:
            keyboard_device: Keyboard device instance
            msg_queue: Message queue instance
        """
        self._keyboard = keyboard_device
        self._msg_queue = msg_queue
        self._state = RF4State.IDLE
        self._time_press = RF4_JIG_PRESS_MS
        self._time_release = RF4_JIG_RELEASE_MS
        
        if msg_queue:
            msg_queue.subscribe("rf4/control", self._handle_command)
    
    def _handle_command(self, msg):
        """
        Handle control command
        
        Command Format:
        - jig;press_ms;release_ms
        - pull;press_ms;release_ms
        - clear
        
        Args:
            msg: Command string
        """
        try:
            parts = msg.split(';')
            cmd = parts[0]
            
            if cmd == "jig":
                self._state = RF4State.JIG
                if len(parts) >= 3:
                    self._time_press = int(parts[1])
                    self._time_release = int(parts[2])
                print(f"[INFO] RF4 JIG mode: {self._time_press}/{self._time_release}ms")
            
            elif cmd == "pull":
                self._state = RF4State.PULL
                if len(parts) >= 3:
                    self._time_press = int(parts[1])
                    self._time_release = int(parts[2])
                print(f"[INFO] RF4 PULL mode: {self._time_press}/{self._time_release}ms")
            
            elif cmd == "clear":
                self._state = RF4State.IDLE
                print("[INFO] RF4 cleared")
            
            else:
                print(f"[WARN] RF4 unknown command: {cmd}")
        except Exception as e:
            print(f"[ERROR] RF4Service._handle_command: {e}")
            import sys
            sys.print_exception(e)
    
    def _random_sleep_ms(self, base_ms):
        """
        Random delay
        
        Args:
            base_ms: Base delay time in milliseconds
        """
        variance = base_ms * RF4_RANDOM_VARIANCE
        delay = random.uniform(base_ms - variance, base_ms + variance)
        time.sleep_ms(int(delay))
    
    def _jig_cycle(self):
        """Execute JIG cycle"""
        try:
            self._keyboard.press(';')
            self._random_sleep_ms(self._time_press)
            self._keyboard.release(';')
            self._random_sleep_ms(self._time_release)
        except Exception as e:
            print(f"[ERROR] RF4Service._jig_cycle: {e}")
            import sys
            sys.print_exception(e)
    
    def _pull_cycle(self):
        """Execute PULL cycle"""
        try:
            self._keyboard.press(';')
            self._keyboard.press("'")
            self._random_sleep_ms(self._time_press)
            self._keyboard.release("'")
            self._random_sleep_ms(self._time_release)
        except Exception as e:
            print(f"[ERROR] RF4Service._pull_cycle: {e}")
            import sys
            sys.print_exception(e)
    
    def run(self):
        """Run service main loop (blocking)"""
        while True:
            try:
                if self._state == RF4State.JIG:
                    self._jig_cycle()
                elif self._state == RF4State.PULL:
                    self._pull_cycle()
                else:
                    time.sleep(2)
            except KeyboardInterrupt:
                print("[INFO] RF4 service stopped")
                break
            except Exception as e:
                print(f"[ERROR] RF4Service.run: {e}")
                import sys
                sys.print_exception(e)
                time.sleep(1)
    
    def set_state(self, state, press_ms=None, release_ms=None):
        """
        Set running state
        
        Args:
            state: State (RF4State.IDLE/JIG/PULL)
            press_ms: Press time in milliseconds
            release_ms: Release time in milliseconds
        """
        self._state = state
        if press_ms is not None:
            self._time_press = press_ms
        if release_ms is not None:
            self._time_release = release_ms
    
    def stop(self):
        """Stop service"""
        self._state = RF4State.IDLE
