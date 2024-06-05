from machine import Pin
import time

# from mouse_example import Device


def test():
    import mouse
    print("test")
    mouse.test()

def start():
    import keyboard
    import rf4
    import wifi
    print("start rf4 ")


led_pin=2
led = Pin(led_pin, Pin.OUT)
for i in range(3):
    led.value(0)
    time.sleep_ms(200)
    led.value(1)
    time.sleep_ms(200)

start()