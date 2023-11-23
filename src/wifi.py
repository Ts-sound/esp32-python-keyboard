import network,time,_thread,time,socket
import msg_queue

ssid = "T"
key = "12345678"

nic = network.WLAN(network.STA_IF)
nic.active(True)
print(nic.scan())
s = socket.socket()
global client

def Send(msg= ""):
    try:
        client.send(msg)    
    except:
        print("send error ")

def main():
    nic.connect(ssid, key)
    while True:
        if not nic.isconnected():
            nic.disconnect()
            nic.connect(ssid, key)
            time.sleep(1)
            print("connect : ",nic.isconnected())
            if(nic.isconnected()):
                print("start listening at 80 ...")
                s.bind(("0.0.0.0", 80))
                s.listen(5)
                client, address = s.accept()
                client.settimeout(10)
        else:
            try:
                if client :
                    data = client.recv(1024)
                    print(data)
                    msg_queue.Publish("wifi/raw",str(data,"utf-8"))
            except Exception as e:
                print(e)
                
    return 0

            
            

_thread.start_new_thread(main,())
print("wifi start")