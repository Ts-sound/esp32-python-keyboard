"""
LED 驱动

提供 LED 状态指示功能。
"""

from machine import Pin
import time


class LEDDriver:
    """
    LED 驱动类
    
    用于控制 ESP32 板载 LED，提供状态指示。
    """
    
    def __init__(self, pin=2):
        """
        初始化 LED 驱动
        
        Args:
            pin: LED 引脚号（默认 2）
        """
        self._pin = Pin(pin, Pin.OUT)
        self._state = 0
    
    def on(self):
        """打开 LED"""
        self._pin.value(1)
        self._state = 1
    
    def off(self):
        """关闭 LED"""
        self._pin.value(0)
        self._state = 0
    
    def toggle(self):
        """切换 LED 状态"""
        self._state = 1 - self._state
        self._pin.value(self._state)
    
    def blink(self, count=3, interval_ms=200):
        """
        闪烁 LED
        
        Args:
            count: 闪烁次数
            interval_ms: 间隔时间（毫秒）
        """
        for _ in range(count):
            self.on()
            time.sleep_ms(interval_ms)
            self.off()
            time.sleep_ms(interval_ms)
    
    def heartbeat(self, interval_ms=1000):
        """
        心跳闪烁（阻塞）
        
        Args:
            interval_ms: 心跳间隔（毫秒）
        """
        self.on()
        time.sleep_ms(100)
        self.off()
        time.sleep_ms(interval_ms - 100)
