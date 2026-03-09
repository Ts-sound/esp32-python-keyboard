import sys
import asyncio

# 路径配置（必须在其他 import 之前）
sys.path.insert(0, '/lib/MicroPythonBLEHID')
sys.path.insert(0, '/src')

from machine import Pin
from config import LED_PIN
from led_driver import blink_led
from keyboard_app import KeyboardApp


async def main_async():
    """Main async entry point"""
    print("[INFO] ESP32 Keyboard starting...")
    blink_led()
    
    led = Pin(LED_PIN, Pin.OUT)
    led.value(1)  # Running indicator
    
    app = KeyboardApp()
    if not app.start():
        print("[ERROR] Failed to start application")
        led.value(0)
        return
    
    try:
        await app.run_async()
    except KeyboardInterrupt:
        print("[INFO] Interrupted by user")
    except Exception as e:
        print(f"[ERROR] Fatal error: {e}")
        import sys
        sys.print_exception(e)
    finally:
        led.value(0)  # Exit indicator
        await app.stop_async()


# Start asyncio event loop
if __name__ == "__main__":
    asyncio.run(main_async())
