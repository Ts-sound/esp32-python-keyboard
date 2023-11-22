import hid_services
import time
import random

keyboard = hid_services.Keyboard()

def keyboard_state_callback():
  return

keyboard.set_state_change_callback(keyboard_state_callback)
keyboard.start()
keyboard.start_advertising()
print("keyboard start")
