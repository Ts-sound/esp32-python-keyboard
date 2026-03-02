"""
键盘设备

提供高级键盘 API，封装 HID 驱动。
支持多键无冲和字符串发送。
"""

import sys
import time

sys.path.append('../drivers')
from hid_driver import HIDDriver
from utils.hid_mapper import HID_KEYMAP


class KeyboardDevice:
    """
    键盘设备类
    
    提供高级键盘 API，支持：
    - 单键按下/释放
    - 多键无冲（最多 6 键）
    - 字符串发送
    - 修饰键支持
    """
    
    def __init__(self, device_name="ESP32-Keyboard"):
        """
        初始化键盘设备
        
        Args:
            device_name: 设备名称
        """
        self._hid = HIDDriver(device_name)
        self._pressed_keys = []
    
    def start(self):
        """
        启动键盘
        
        Returns:
            bool: 是否成功
        """
        return self._hid.start()
    
    def start_advertising(self):
        """
        开始广播
        
        Returns:
            bool: 是否成功
        """
        return self._hid.start_advertising()
    
    def stop_advertising(self):
        """
        停止广播
        
        Returns:
            bool: 是否成功
        """
        return self._hid.stop_advertising()
    
    def press(self, key):
        """
        按下按键
        
        Args:
            key: 按键名称（如 'a', 'enter', 'F1'）
            
        Returns:
            bool: 是否成功
        """
        try:
            if key not in HID_KEYMAP:
                print(f"[WARN] Unknown key: {key}")
                return False
            
            code = HID_KEYMAP[key]
            if code not in self._pressed_keys:
                self._pressed_keys.append(code)
            return self._send_report()
        except Exception as e:
            print(f"[ERROR] KeyboardDevice.press: {e}")
            sys.print_exception(e)
            return False
    
    def release(self, key):
        """
        释放按键
        
        Args:
            key: 按键名称
            
        Returns:
            bool: 是否成功
        """
        try:
            if key not in HID_KEYMAP:
                return False
            
            code = HID_KEYMAP[key]
            if code in self._pressed_keys:
                self._pressed_keys.remove(code)
            return self._send_report()
        except Exception as e:
            print(f"[ERROR] KeyboardDevice.release: {e}")
            sys.print_exception(e)
            return False
    
    def release_all(self):
        """
        释放所有按键
        
        Returns:
            bool: 是否成功
        """
        try:
            self._pressed_keys = []
            return self._hid.release_all()
        except Exception as e:
            print(f"[ERROR] KeyboardDevice.release_all: {e}")
            sys.print_exception(e)
            return False
    
    def send_string(self, text):
        """
        发送字符串
        
        Args:
            text: 要发送的字符串
            
        Returns:
            bool: 是否成功
        """
        try:
            for char in text:
                char_lower = char.lower()
                is_upper = char.isupper()
                
                if char_lower not in HID_KEYMAP:
                    print(f"[WARN] Unknown char: {char}")
                    continue
                
                code = HID_KEYMAP[char_lower]
                
                if is_upper:
                    self._hid.send_keys([code], {'left_shift': 1})
                else:
                    self._hid.send_keys([code])
                
                time.sleep_ms(20)
                self._hid.release_all()
                time.sleep_ms(20)
            
            return True
        except Exception as e:
            print(f"[ERROR] KeyboardDevice.send_string: {e}")
            sys.print_exception(e)
            return False
    
    def set_modifiers(self, **kwargs):
        """
        设置修饰键
        
        Args:
            left_control, left_shift, left_alt, left_gui,
            right_control, right_shift, right_alt, right_gui
            
        Returns:
            bool: 是否成功
        """
        try:
            self._hid.send_keys(self._pressed_keys[:6], kwargs)
            return True
        except Exception as e:
            print(f"[ERROR] KeyboardDevice.set_modifiers: {e}")
            sys.print_exception(e)
            return False
    
    def _send_report(self):
        """发送 HID 报告"""
        return self._hid.send_keys(self._pressed_keys[:6])
    
    def is_connected(self):
        """
        检查是否已连接
        
        Returns:
            bool: 连接状态
        """
        return self._hid.is_connected()
    
    def set_battery_level(self, level):
        """
        设置电池电量
        
        Args:
            level: 电量百分比（0-100）
        """
        self._hid.set_battery_level(level)
    
    def notify_battery_level(self):
        """通知电池电量"""
        self._hid.notify_battery_level()
