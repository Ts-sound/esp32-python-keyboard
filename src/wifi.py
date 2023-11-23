import network,time,_thread,time,socket
import msg_queue

ssid = "T"
key = "12345678"

nic = network.WLAN(network.STA_IF)
nic.active(True)
s = socket.socket()
s.listen(5)
client, address = s.accept()

def Send(msg= ""):
    try:
        client.send(msg)    
    except:
        print("send error ")

def main():
    nic.connect(ssid, key)
    while True:
        if nic.disconnect():
            time.sleep(1)
            nic.connect(ssid, key)
        else:
            try:
                data = client.recv(1024)
                msg_queue.Publish("wifi/recv",str(data,encoding = "utf-8"))
            except:
                print("recv error")
                print("reconnecting ...")
                client, address = s.accept()
            
            

_thread.start_new_thread(main)