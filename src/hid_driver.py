"""
HID 驱动封装

封装外部 MicroPythonBLEHID 库的 hid_services 模块。
提供统一的错误处理和状态检查。
"""

import sys

from hid_services import Keyboard as HIDKeyboard
from hid_services import Mouse as HIDMouse


class HIDDriver:
    """
    HID 驱动封装类
    
    封装 BLE HID Keyboard 服务，提供简化的 API。
    """
    
    def __init__(self, device_name="ESP32-Keyboard"):
        """
        初始化 HID 驱动
        
        Args:
            device_name: 设备名称
        """
        self._keyboard = HIDKeyboard(device_name)
        self._connected = False
        self._setup_callbacks()
    
    def _setup_callbacks(self):
        """设置回调"""
        self._keyboard.set_state_change_callback(self._on_state_change)
    
    def _on_state_change(self):
        """状态变化回调"""
        state = self._keyboard.get_state()
        print(f"[INFO] HID state changed: {state}")
    
    def start(self):
        """
        启动 HID 服务
        
        Returns:
            bool: 是否启动成功
        """
        try:
            self._keyboard.start()
            return True
        except Exception as e:
            print(f"[ERROR] HIDDriver.start: {e}")
            sys.print_exception(e)
            return False
    
    def start_advertising(self):
        """
        开始广播
        
        Returns:
            bool: 是否成功
        """
        try:
            self._keyboard.start_advertising()
            return True
        except Exception as e:
            print(f"[ERROR] HIDDriver.start_advertising: {e}")
            sys.print_exception(e)
            return False
    
    def stop_advertising(self):
        """
        停止广播
        
        Returns:
            bool: 是否成功
        """
        try:
            self._keyboard.stop_advertising()
            return True
        except Exception as e:
            print(f"[ERROR] HIDDriver.stop_advertising: {e}")
            sys.print_exception(e)
            return False
    
    def send_keys(self, keys=None, modifiers=None):
        """
        发送按键
        
        Args:
            keys: 按键码列表（最多 6 个）
            modifiers: 修饰符字典
            
        Returns:
            bool: 是否成功
        """
        try:
            self._keyboard.set_keys()
            self._keyboard.set_modifiers()
            
            if keys and len(keys) > 0:
                self._keyboard.set_keys(*keys[:6])
            if modifiers:
                self._keyboard.set_modifiers(**modifiers)
            
            self._keyboard.notify_hid_report()
            return True
        except Exception as e:
            print(f"[ERROR] HIDDriver.send_keys: {e}")
            sys.print_exception(e)
            return False
    
    def release_all(self):
        """
        释放所有按键
        
        Returns:
            bool: 是否成功
        """
        try:
            self._keyboard.set_keys()
            self._keyboard.set_modifiers()
            self._keyboard.notify_hid_report()
            return True
        except Exception as e:
            print(f"[ERROR] HIDDriver.release_all: {e}")
            sys.print_exception(e)
            return False
    
    def set_battery_level(self, level):
        """
        设置电池电量
        
        Args:
            level: 电量百分比（0-100）
        """
        try:
            self._keyboard.set_battery_level(level)
        except Exception as e:
            print(f"[ERROR] HIDDriver.set_battery_level: {e}")
            sys.print_exception(e)
    
    def notify_battery_level(self):
        """通知电池电量"""
        try:
            self._keyboard.notify_battery_level()
        except Exception as e:
            print(f"[ERROR] HIDDriver.notify_battery_level: {e}")
            sys.print_exception(e)
    
    def is_connected(self):
        """
        检查是否已连接
        
        Returns:
            bool: 连接状态
        """
        return self._keyboard.get_state() == HIDKeyboard.DEVICE_CONNECTED


class MouseDriver:
    """
    HID 鼠标驱动封装类
    """
    
    def __init__(self, device_name="ESP32-Mouse"):
        """
        初始化鼠标驱动
        
        Args:
            device_name: 设备名称
        """
        self._mouse = HIDMouse(device_name)
        self._setup_callbacks()
    
    def _setup_callbacks(self):
        """设置回调"""
        self._mouse.set_state_change_callback(self._on_state_change)
    
    def _on_state_change(self):
        """状态变化回调"""
        print(f"[INFO] Mouse state changed: {self._mouse.get_state()}")
    
    def start(self):
        """启动鼠标服务"""
        try:
            self._mouse.start()
            return True
        except Exception as e:
            print(f"[ERROR] MouseDriver.start: {e}")
            sys.print_exception(e)
            return False
    
    def start_advertising(self):
        """开始广播"""
        try:
            self._mouse.start_advertising()
            return True
        except Exception as e:
            print(f"[ERROR] MouseDriver.start_advertising: {e}")
            sys.print_exception(e)
            return False
    
    def set_buttons(self, b1=0, b2=0, b3=0):
        """
        设置鼠标按钮
        
        Args:
            b1: 左键（0/1）
            b2: 中键（0/1）
            b3: 右键（0/1）
        """
        try:
            self._mouse.set_buttons(b1, b2, b3)
            self._mouse.notify_hid_report()
        except Exception as e:
            print(f"[ERROR] MouseDriver.set_buttons: {e}")
            sys.print_exception(e)
    
    def move(self, x=0, y=0, wheel=0):
        """
        移动鼠标
        
        Args:
            x: X 轴位移（-127 到 127）
            y: Y 轴位移（-127 到 127）
            wheel: 滚轮位移（-127 到 127）
        """
        try:
            self._mouse.move(x, y, wheel)
            self._mouse.notify_hid_report()
        except Exception as e:
            print(f"[ERROR] MouseDriver.move: {e}")
            sys.print_exception(e)
    
    def is_connected(self):
        """检查是否已连接"""
        return self._mouse.get_state() == HIDMouse.DEVICE_CONNECTED
