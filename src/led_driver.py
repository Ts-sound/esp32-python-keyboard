"""
LED Driver

Provides LED status indication functionality.
"""

from machine import Pin
import time


def blink_led(count=3, interval_ms=200):
    """
    Blink LED indication
    
    Args:
        count: Number of blinks
        interval_ms: Interval in milliseconds
    """
    led = Pin(2, Pin.OUT)
    for _ in range(count):
        led.value(0)
        time.sleep_ms(interval_ms)
        led.value(1)
        time.sleep_ms(interval_ms)


class LEDDriver:
    """
    LED Driver Class
    
    Controls ESP32 onboard LED for status indication.
    """
    
    def __init__(self, pin=2):
        """
        Initialize LED driver
        
        Args:
            pin: LED pin number (default 2)
        """
        self._pin = Pin(pin, Pin.OUT)
        self._state = 0
    
    def on(self):
        """Turn on LED"""
        self._pin.value(1)
        self._state = 1
    
    def off(self):
        """Turn off LED"""
        self._pin.value(0)
        self._state = 0
    
    def toggle(self):
        """Toggle LED state"""
        self._state = 1 - self._state
        self._pin.value(self._state)
    
    def blink(self, count=3, interval_ms=200):
        """
        Blink LED
        
        Args:
            count: Number of blinks
            interval_ms: Interval in milliseconds
        """
        for _ in range(count):
            self.on()
            time.sleep_ms(interval_ms)
            self.off()
            time.sleep_ms(interval_ms)
    
    def heartbeat(self, interval_ms=1000):
        """
        Heartbeat blink (blocking)
        
        Args:
            interval_ms: Heartbeat interval in milliseconds
        """
        self.on()
        time.sleep_ms(100)
        self.off()
        time.sleep_ms(interval_ms - 100)
