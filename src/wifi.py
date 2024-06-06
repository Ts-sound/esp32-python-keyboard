import network,time,_thread,time,socket
import msg_queue

ssid = "T"
key = "12345678"

nic = network.WLAN(network.STA_IF)
nic.active(True)

# 如果已经连接，则断开连接
if nic.isconnected():
    nic.disconnect()

# 设置固定 IP 地址
nic.ifconfig(('192.168.137.5', '255.255.255.0', '192.168.137.1', '8.8.8.8'))

print(nic.scan())

s = socket.socket()
global client

def Send(msg= ""):
    try:
        client.send(msg)    
    except:
        print("send error ")

def do_connect():
    global nic
    if not nic.isconnected():
        print('connecting to network...')
        nic.connect(ssid, key)
        while not nic.isconnected():
            pass
    print('network config:', nic.ifconfig())

def main():
    nic.connect(ssid, key)
    time.sleep(5)
    while True:
        if not nic.isconnected():
            do_connect()
            if(nic.isconnected()):
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