"""
ESP32 Keyboard Main Entry Point

Starts keyboard application, initializes all components and runs main loop.
"""

from machine import Pin
import time

from config import LED_PIN, LED_BLINK_COUNT, LED_BLINK_INTERVAL_MS
from keyboard_app import KeyboardApp


def blink_led(count=LED_BLINK_COUNT, interval_ms=LED_BLINK_INTERVAL_MS):
    """LED blink indication"""
    led = Pin(LED_PIN, Pin.OUT)
    for _ in range(count):
        led.value(0)
        time.sleep_ms(interval_ms)
        led.value(1)
        time.sleep_ms(interval_ms)


def main():
    """Main function"""
    print("[INFO] ESP32 Keyboard starting...")
    blink_led()
    
    app = KeyboardApp()
    
    if not app.start():
        print("[ERROR] Failed to start application")
        Pin(LED_PIN, Pin.OUT).value(0)  # Turn off LED on error
        return
    
    # Turn on LED to indicate running
    Pin(LED_PIN, Pin.OUT).value(1)
    
    try:
        app.run()
    finally:
        # Turn off LED on exit
        Pin(LED_PIN, Pin.OUT).value(0)


if __name__ == "__main__":
    main()
