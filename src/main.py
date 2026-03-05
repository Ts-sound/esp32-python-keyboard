"""
ESP32 Keyboard 主入口

启动键盘应用，初始化所有组件并运行主循环。
"""

from machine import Pin
import time

from config import LED_PIN, LED_BLINK_COUNT, LED_BLINK_INTERVAL_MS
from keyboard_app import KeyboardApp


def blink_led(count=LED_BLINK_COUNT, interval_ms=LED_BLINK_INTERVAL_MS):
    """LED 闪烁指示"""
    led = Pin(LED_PIN, Pin.OUT)
    for _ in range(count):
        led.value(0)
        time.sleep_ms(interval_ms)
        led.value(1)
        time.sleep_ms(interval_ms)


def main():
    """主函数"""
    print("[INFO] ESP32 Keyboard starting...")
    blink_led()
    
    app = KeyboardApp()
    
    if not app.start():
        print("[ERROR] Failed to start application")
        return
    
    blink_led()
    app.run()


if __name__ == "__main__":
    main()
