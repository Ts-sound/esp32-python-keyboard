import network,time,_thread,time,socket
import msg_queue

ssid = "T"
key = "12345678"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
time.sleep(4)

# 设置固定 IP 地址
# nic.ifconfig(('192.168.137.5', '255.255.255.0', '192.168.137.1', '8.8.8.8'))

# print(nic.scan())

s = socket.socket()
client=None

def Send(msg= ""):
    global client
    try:
        client.send(msg)    
    except:
        print("send error ")

def do_connect():
    global wlan
    print( wlan.scan())
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, key)
        while not wlan.isconnected():
            time.sleep(2)
            print('connecting...')
            pass
    print('network config:', wlan.ifconfig())

def main():
    global client,wlan
    while True:
        if not wlan.isconnected():
            do_connect()
            if(wlan.isconnected()):
                print("start listening at 80 ...")
                s.bind(("0.0.0.0", 80))
                s.listen(5)
                client, address = s.accept()
                client.settimeout(1800)
        else:
            try:
                if client :
                    data = client.recv(1024)
                    print(data)
                    msg_queue.Publish("wifi/raw",str(data,"utf-8"))
            except Exception as e:
                print(e)
                client, address = s.accept()
                client.settimeout(1800)
                
    return 0

            
            

_thread.start_new_thread(main,())
print("wifi start")