"""
boot.py -- run on boot-up
"""

import sys
import time
from machine import Pin

from config import LED_PIN

sys.path.insert(0, '/lib/MicroPythonBLEHID')
sys.path.insert(0, '/src')

# Turn on LED to indicate boot
led = Pin(LED_PIN, Pin.OUT)
led.value(1)

# Delay to allow interrupt via Ctrl+C (5 seconds)
print("[BOOT] Press Ctrl+C within 5s to interrupt...")
for i in range(5, 0, -1):
    print(f"[BOOT] Starting in {i}s...")
    time.sleep_ms(1000)

try:
    import main
    main.main()
except KeyboardInterrupt:
    print("[BOOT] Interrupted by user - REPL available")
    led.value(0)  # Turn off LED on interrupt
