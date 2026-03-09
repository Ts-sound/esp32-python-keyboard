import sys

# 路径配置（必须在其他 import 之前）
sys.path.insert(0, '/lib/MicroPythonBLEHID')
sys.path.insert(0, '/src')

from machine import Pin
from config import LED_PIN
from led_driver import blink_led
from keyboard_app import KeyboardApp


def main():
    print("[INFO] ESP32 Keyboard starting...")
    blink_led()
    
    led = Pin(LED_PIN, Pin.OUT)
    led.value(1)  # 运行中亮灯
    
    app = KeyboardApp()
    if not app.start():
        print("[ERROR] Failed to start application")
        led.value(0)
        return
    
    try:
        app.run()
    finally:
        led.value(0)  # 退出关灯


if __name__ == "__main__":
    main()
