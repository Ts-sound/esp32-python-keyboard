"""
鼠标设备

提供高级鼠标 API，封装 HID 驱动。
"""

import time

from hid_driver import MouseDriver


class MouseDevice:
    """
    鼠标设备类
    
    提供高级鼠标 API，支持：
    - 鼠标按钮按下/释放
    - 鼠标移动
    - 滚轮滚动
    """
    
    def __init__(self, device_name="ESP32-Mouse"):
        """
        初始化鼠标设备
        
        Args:
            device_name: 设备名称
        """
        self._hid = MouseDriver(device_name)
        self._buttons = [0, 0, 0]
    
    def start(self):
        """
        启动鼠标
        
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
    
    def click(self, button="left"):
        """
        点击鼠标按钮
        
        Args:
            button: 按钮名称（'left', 'middle', 'right'）
        """
        try:
            if button == "left":
                idx = 0
            elif button == "middle":
                idx = 1
            elif button == "right":
                idx = 2
            else:
                print(f"[WARN] Unknown button: {button}")
                return
            
            self._buttons[idx] = 1
            self._hid.set_buttons(*self._buttons)
            time.sleep_ms(50)
            self._buttons[idx] = 0
            self._hid.set_buttons(*self._buttons)
        except Exception as e:
            print(f"[ERROR] MouseDevice.click: {e}")
            sys.print_exception(e)
    
    def press(self, button="left"):
        """
        按下鼠标按钮
        
        Args:
            button: 按钮名称
        """
        try:
            if button == "left":
                idx = 0
            elif button == "middle":
                idx = 1
            elif button == "right":
                idx = 2
            else:
                print(f"[WARN] Unknown button: {button}")
                return
            
            self._buttons[idx] = 1
            self._hid.set_buttons(*self._buttons)
        except Exception as e:
            print(f"[ERROR] MouseDevice.press: {e}")
            sys.print_exception(e)
    
    def release(self, button="left"):
        """
        释放鼠标按钮
        
        Args:
            button: 按钮名称
        """
        try:
            if button == "left":
                idx = 0
            elif button == "middle":
                idx = 1
            elif button == "right":
                idx = 2
            else:
                print(f"[WARN] Unknown button: {button}")
                return
            
            self._buttons[idx] = 0
            self._hid.set_buttons(*self._buttons)
        except Exception as e:
            print(f"[ERROR] MouseDevice.release: {e}")
            sys.print_exception(e)
    
    def move(self, x=0, y=0):
        """
        移动鼠标
        
        Args:
            x: X 轴位移（-127 到 127）
            y: Y 轴位移（-127 到 127）
        """
        try:
            self._hid.move(x=x, y=y)
        except Exception as e:
            print(f"[ERROR] MouseDevice.move: {e}")
            sys.print_exception(e)
    
    def scroll(self, steps=1):
        """
        滚动滚轮
        
        Args:
            steps: 滚动步数（正数向上，负数向下）
        """
        try:
            self._hid.move(wheel=steps)
        except Exception as e:
            print(f"[ERROR] MouseDevice.scroll: {e}")
            sys.print_exception(e)
    
    def is_connected(self):
        """
        检查是否已连接
        
        Returns:
            bool: 连接状态
        """
        return self._hid.is_connected()
