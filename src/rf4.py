import msg_queue,_thread,time,random
import keyboard

class State():
  IDEL=0
  JIG=1

state = State()
state = State.IDEL
_time_ms = [1135,1985]

def Handle(msg=""):
  global _time_ms,state

  strs = msg.split(";")
  print(strs)
  try:
    if(strs[0] == "jig"):
        state = State.JIG
        _time_ms[0] = int(strs[1])
        _time_ms[1] = int(strs[2])
    elif(strs[0] == "clear"):
      state = State.IDEL
    else:
        print ("rf4 not handle: ",msg)
  except Exception as e:
    print("rf4 except ",e)

def Sleep_ms(time_ms:float):
    t = random.uniform(time_ms*0.8,time_ms*1.2)
    t/=1000 # ms -> s
    time.sleep(t)

msg_queue.Subscribe("wifi/raw",Handle)

def Jig():
    keyboard.Handle(";")
    Sleep_ms(_time_ms[0])
    keyboard.Handle("clear")
    Sleep_ms(84)

    keyboard.Handle("enter")
    Sleep_ms(36)
    keyboard.Handle("clear")
    Sleep_ms(_time_ms[1])
  

def main():
  
  while(True):
    if(state == State.JIG):
      Jig()
    else:
      time.sleep(2)

  return 0

_thread.start_new_thread(main,())
print("rf4 start")