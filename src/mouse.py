import hid_services
import time
import random

mouse = hid_services.Mouse()

def mouse_state_callback():
  return

mouse.set_state_change_callback(mouse_state_callback)
mouse.start()
mouse.start_advertising()
print("mouse start")

time.sleep(60)

def send(b1=0,b2=0,b3=0):
  if(mouse.is_connected()):
    mouse.set_buttons(b1,b2,b3)
    mouse.notify_hid_report()
    time.sleep_ms(50)
    
def test():
  for i in range(30):
    print("test : ",i)
    # send(1,0,0)
    # time.sleep(1)
    # send(0,1,0)
    # time.sleep(1)
    # send(0,0,1)
    time.sleep(1)
    mouse.set_battery_level(50)
    mouse.notify_battery_level()
