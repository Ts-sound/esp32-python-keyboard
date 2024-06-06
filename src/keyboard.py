import hid_services,msg_queue
import time,_thread
import random

a = [()]

keys = [0,0]
shift = 0
ctrl = 0

keyboard = hid_services.Keyboard()

def keyboard_state_callback():
  return

keyboard.set_state_change_callback(keyboard_state_callback)
keyboard.start()
keyboard.start_advertising()
print("keyboard start")

def get_ket_val(char=""):
  key=0
  if char == " ":
      key = 0x2C
  elif char == "":
     key = 0
  elif char == "enter":
     key = 0x28
  elif char == ";":
     key = 0x33
  elif char == "'":
     key = 0x34
  elif ord("a") <= ord(char) <= ord("z"):
      key = 0x04 + ord(char) - ord("a")
  else:
     key=0
  
  return key

def send_key():
  time.sleep_ms(20)
  print(" key = ",keys," shift = ",shift," ctrl = ",ctrl)
  keyboard.set_keys(keys[0],keys[1])
  keyboard.set_modifiers(left_shift=shift,left_control=ctrl)
  keyboard.notify_hid_report()
  time.sleep_ms(20)

def Handle(msg="",key1="",key2=""):
  global keys,shift,ctrl
  if(msg == "shift"):
    shift = 1
  elif(msg == "ctrl"):
    ctrl = 1
  elif(msg == "clear"):
     shift=ctrl=keys[0]=keys[1]=0
  else:
    try:
      keys[0] = get_ket_val(key1)
      keys[1] = get_ket_val(key2)
    except Exception as e:
      print("keyboard exept : ",e)

  if(keys[0] >=0):
    send_key()
     

msg_queue.Subscribe("wifi/raw",Handle)
print("keyboard")