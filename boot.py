"""
boot.py -- run on boot-up
"""

import sys
import time
import select
from machine import Pin

# Add src and lib paths first
sys.path.insert(0, '/lib/MicroPythonBLEHID')
sys.path.insert(0, '/src')

# Now import from config
from config import LED_PIN

# Turn on LED to indicate boot
led = Pin(LED_PIN, Pin.OUT)
led.value(1)

# Delay to allow interrupt (5 seconds)
# Check stdin during countdown using non-blocking select
print("[BOOT] Press any key within 5s to interrupt...")
for i in range(5, 0, -1):
    print(f"[BOOT] Starting in {i}s...")
    time.sleep_ms(1000)
    
    # Non-blocking check for stdin input
    if select.select([sys.stdin], [], [], 0)[0]:
        # Drain any pending input
        sys.stdin.read(1)
        print("[BOOT] Input detected - skipping auto-start, REPL available")
        led.value(0)  # Turn off LED
        sys.exit()  # Exit boot, REPL remains available

try:
    import main
    main.main()
except KeyboardInterrupt:
    print("[BOOT] Interrupted by user - REPL available")
    led.value(0)
