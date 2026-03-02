"""
WiFi 服务

封装 ESP32 WiFi 功能，提供 TCP 服务器和客户端通信。
支持自动重连和消息队列集成。
"""

import network
import socket
import time

from config.config import (
    WIFI_SSID,
    WIFI_PASSWORD,
    WIFI_PORT,
    WIFI_TIMEOUT_SEC,
    WIFI_SOCKET_TIMEOUT_SEC,
)


class WiFiService:
    """
    WiFi 服务类
    
    提供：
    - WiFi 连接管理
    - TCP 服务器
    - 客户端通信
    - 消息队列集成
    """
    
    def __init__(self, msg_queue=None):
        """
        初始化 WiFi 服务
        
        Args:
            msg_queue: 消息队列实例
        """
        self._wlan = network.WLAN(network.STA_IF)
        self._socket = None
        self._client = None
        self._msg_queue = msg_queue
        self._connected = False
    
    def start(self):
        """
        启动 WiFi
        
        Returns:
            bool: 是否成功
        """
        try:
            self._wlan.active(True)
            print("[INFO] WiFi activated")
            return True
        except Exception as e:
            print(f"[ERROR] WiFiService.start: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def connect(self):
        """
        连接到 WiFi
        
        Returns:
            bool: 是否连接成功
        """
        try:
            print(f"[INFO] Connecting to {WIFI_SSID}...")
            self._wlan.connect(WIFI_SSID, WIFI_PASSWORD)
            
            timeout = time.time() + WIFI_TIMEOUT_SEC
            while time.time() < timeout:
                if self._wlan.isconnected():
                    self._connected = True
                    print(f"[INFO] Connected: {self._wlan.ifconfig()}")
                    return True
                time.sleep(1)
            
            print("[ERROR] WiFi connection timeout")
            return False
        except Exception as e:
            print(f"[ERROR] WiFiService.connect: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def reconnect(self):
        """
        重新连接 WiFi
        
        Returns:
            bool: 是否成功
        """
        try:
            if self._wlan.isconnected():
                self._wlan.disconnect()
            time.sleep(1)
            return self.connect()
        except Exception as e:
            print(f"[ERROR] WiFiService.reconnect: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def start_server(self):
        """
        启动 TCP 服务器
        
        Returns:
            bool: 是否成功
        """
        try:
            self._socket = socket.socket()
            self._socket.bind(('0.0.0.0', WIFI_PORT))
            self._socket.listen(5)
            print(f"[INFO] Server listening on port {WIFI_PORT}")
            return True
        except Exception as e:
            print(f"[ERROR] WiFiService.start_server: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def accept_client(self):
        """
        接受客户端连接
        
        Returns:
            bool: 是否成功
        """
        try:
            if self._socket:
                self._client, addr = self._socket.accept()
                self._client.settimeout(WIFI_SOCKET_TIMEOUT_SEC)
                print(f"[INFO] Client connected: {addr}")
                return True
            return False
        except Exception as e:
            print(f"[ERROR] WiFiService.accept_client: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def recv_data(self, buffer_size=1024):
        """
        接收数据
        
        Args:
            buffer_size: 缓冲区大小
            
        Returns:
            str: 接收的数据，或 None
        """
        try:
            if self._client:
                data = self._client.recv(buffer_size)
                if data:
                    msg = data.decode('utf-8')
                    if self._msg_queue:
                        self._msg_queue.publish("wifi/raw", msg)
                    return msg
            return None
        except Exception as e:
            print(f"[ERROR] WiFiService.recv_data: {e}")
            import sys
            sys.print_exception(e)
            return None
    
    def send_data(self, data):
        """
        发送数据
        
        Args:
            data: 要发送的数据
            
        Returns:
            bool: 是否成功
        """
        try:
            if self._client:
                self._client.send(data.encode('utf-8'))
                return True
            return False
        except Exception as e:
            print(f"[ERROR] WiFiService.send_data: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def is_connected(self):
        """
        检查连接状态
        
        Returns:
            bool: 连接状态
        """
        return self._wlan.isconnected() and self._connected
    
    def get_ip(self):
        """
        获取 IP 地址
        
        Returns:
            tuple: (ip, netmask, gateway, dns) 或 None
        """
        try:
            if self._wlan.isconnected():
                return self._wlan.ifconfig()
            return None
        except Exception as e:
            print(f"[ERROR] WiFiService.get_ip: {e}")
            import sys
            sys.print_exception(e)
            return None
    
    def close(self):
        """关闭连接"""
        try:
            if self._client:
                self._client.close()
                self._client = None
            if self._socket:
                self._socket.close()
                self._socket = None
            print("[INFO] WiFi connection closed")
        except Exception as e:
            print(f"[ERROR] WiFiService.close: {e}")
            import sys
            sys.print_exception(e)
