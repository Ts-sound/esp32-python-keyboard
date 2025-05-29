import msg_queue,_thread,time,random
import keyboard

class State():
  IDEL=0
  JIG=1
  PULL=2

state = State()
state = State.IDEL
_time_ms = [1135,1985]

def Handle(msg=""):
  global _time_ms,state

  strs = msg.split(";")
  print(strs)
  try:
    if(strs[0] == "jig"): #jig;800;500
        state = State.JIG
        _time_ms[0] = int(strs[1])
        _time_ms[1] = int(strs[2])
    if(strs[0] == "pull"): #pull;800;500
        state = State.PULL
        _time_ms[0] = int(strs[1])
        _time_ms[1] = int(strs[2])
    elif(strs[0] == "clear"):
      state = State.IDEL
    else:
        print ("rf4 not handle: ",msg)
  except Exception as e:
    print("rf4 except ",e)

def Sleep_ms(time_ms:float):
    t = random.uniform(time_ms*0.9,time_ms*1.1)
    t/=1000 # ms -> s
    time.sleep(t)

msg_queue.Subscribe("wifi/raw",Handle)

def Jig():
    keyboard.Handle("",";")
    Sleep_ms(_time_ms[0])
    keyboard.Handle("clear")
    Sleep_ms(_time_ms[1])

    # keyboard.Handle("","enter")
    # Sleep_ms(124)
    # keyboard.Handle("clear")
    # Sleep_ms(_time_ms[1])
  
def Pull():
    keyboard.Handle("",";")
    Sleep_ms(84)
    
    cnt = 20
    while cnt:
      cnt -=1
      keyboard.Handle("",";","'")
      Sleep_ms(_time_ms[0])
      keyboard.Handle("",";")
      Sleep_ms(_time_ms[1])

    global state
    state = State.IDEL
  

def main():
  
  while(True):
    if(state == State.JIG):
      Jig()
    elif(state == State.PULL):
      Pull()
    else:
      time.sleep(2)

  return 0

_thread.start_new_thread(main,())
print("rf4 start")