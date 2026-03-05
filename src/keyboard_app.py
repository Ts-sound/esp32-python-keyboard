"""
键盘应用

应用层逻辑，协调各服务层模块。
"""

import time

from config import (
    HID_ADVERTISING_TIMEOUT_SEC,
    MAIN_LOOP_INTERVAL_MS,
)
from keyboard_device import KeyboardDevice
from rf4_service import RF4Service
from wifi_service import WiFiService
from msg_queue import MessageQueue


class KeyboardApp:
    """
    键盘应用类
    
    协调所有服务和设备，提供统一的应用入口。
    """
    
    def __init__(self):
        """初始化应用"""
        self._msg_queue = None
        self._keyboard = None
        self._wifi = None
        self._rf4 = None
        self._running = False
    
    def init(self):
        """
        初始化所有组件
        
        Returns:
            bool: 是否成功
        """
        print("[INFO] Initializing components...")
        
        try:
            # 1. 消息队列
            self._msg_queue = MessageQueue(max_size=10)
            print("[INFO] MessageQueue initialized")
            
            # 2. 键盘设备
            self._keyboard = KeyboardDevice()
            if not self._keyboard.start():
                print("[ERROR] Failed to start keyboard")
                return False
            print("[INFO] Keyboard started")
            
            # 3. WiFi 服务
            self._wifi = WiFiService(msg_queue=self._msg_queue)
            if not self._wifi.start():
                print("[ERROR] Failed to start WiFi")
                return False
            print("[INFO] WiFi started")
            
            # 4. RF4 服务
            self._rf4 = RF4Service(
                keyboard_device=self._keyboard,
                msg_queue=self._msg_queue
            )
            print("[INFO] RF4 service initialized")
            
            return True
        except Exception as e:
            print(f"[ERROR] KeyboardApp.init: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def start(self):
        """
        启动应用主循环
        
        Returns:
            bool: 是否成功
        """
        if not self.init():
            return False
        
        self._running = True
        
        # 启动键盘广播
        self._keyboard.start_advertising()
        print("[INFO] Keyboard advertising started")
        
        # 启动 WiFi 连接
        if self._wifi.connect():
            if self._wifi.start_server():
                print("[INFO] WiFi server ready")
        
        print("[INFO] Application started")
        return True
    
    def run(self):
        """运行主循环（阻塞）"""
        try:
            while self._running:
                # WiFi 数据接收（非阻塞）
                if self._wifi.is_connected():
                    data = self._wifi.recv_data()
                    if data:
                        print(f"[RECV] {data}")
                
                # RF4 状态检查（非阻塞）
                # RF4 服务有自己的内部循环，这里只处理消息
                
                time.sleep_ms(MAIN_LOOP_INTERVAL_MS)
        except KeyboardInterrupt:
            print("[INFO] Stopping...")
        except Exception as e:
            print(f"[ERROR] KeyboardApp.run: {e}")
            import sys
            sys.print_exception(e)
        finally:
            self.stop()
    
    def stop(self):
        """停止应用"""
        print("[INFO] Stopping application...")
        self._running = False
        
        if self._wifi:
            self._wifi.close()
        
        print("[INFO] Application stopped")
    
    def get_keyboard(self):
        """获取键盘设备"""
        return self._keyboard
    
    def get_wifi(self):
        """获取 WiFi 服务"""
        return self._wifi
    
    def get_rf4(self):
        """获取 RF4 服务"""
        return self._rf4
    
    def get_msg_queue(self):
        """获取消息队列"""
        return self._msg_queue
