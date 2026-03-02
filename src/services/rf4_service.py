"""
RF4 服务

实现 RF4 自动按键功能，支持 JIG 和 PULL 两种模式。
通过消息队列接收控制命令。
"""

import time
import random

from config.config import (
    RF4_JIG_PRESS_MS,
    RF4_JIG_RELEASE_MS,
    RF4_PULL_PRESS_MS,
    RF4_PULL_RELEASE_MS,
    RF4_RANDOM_VARIANCE,
)


class RF4State:
    """RF4 状态枚举"""
    IDLE = 0
    JIG = 1
    PULL = 2


class RF4Service:
    """
    RF4 服务类
    
    提供：
    - JIG 模式：自动按压分号键
    - PULL 模式：自动按压分号和单引号键
    - 消息队列控制接口
    - 随机延迟防检测
    """
    
    def __init__(self, keyboard_device, msg_queue=None):
        """
        初始化 RF4 服务
        
        Args:
            keyboard_device: 键盘设备实例
            msg_queue: 消息队列实例
        """
        self._keyboard = keyboard_device
        self._msg_queue = msg_queue
        self._state = RF4State.IDLE
        self._time_press = RF4_JIG_PRESS_MS
        self._time_release = RF4_JIG_RELEASE_MS
        
        if msg_queue:
            msg_queue.subscribe("rf4/control", self._handle_command)
    
    def _handle_command(self, msg):
        """
        处理控制命令
        
        命令格式:
        - jig;press_ms;release_ms
        - pull;press_ms;release_ms
        - clear
        
        Args:
            msg: 命令字符串
        """
        try:
            parts = msg.split(';')
            cmd = parts[0]
            
            if cmd == "jig":
                self._state = RF4State.JIG
                if len(parts) >= 3:
                    self._time_press = int(parts[1])
                    self._time_release = int(parts[2])
                print(f"[INFO] RF4 JIG mode: {self._time_press}/{self._time_release}ms")
            
            elif cmd == "pull":
                self._state = RF4State.PULL
                if len(parts) >= 3:
                    self._time_press = int(parts[1])
                    self._time_release = int(parts[2])
                print(f"[INFO] RF4 PULL mode: {self._time_press}/{self._time_release}ms")
            
            elif cmd == "clear":
                self._state = RF4State.IDLE
                print("[INFO] RF4 cleared")
            
            else:
                print(f"[WARN] RF4 unknown command: {cmd}")
        except Exception as e:
            print(f"[ERROR] RF4Service._handle_command: {e}")
            import sys
            sys.print_exception(e)
    
    def _random_sleep_ms(self, base_ms):
        """
        随机延迟
        
        Args:
            base_ms: 基础延迟时间（毫秒）
        """
        variance = base_ms * RF4_RANDOM_VARIANCE
        delay = random.uniform(base_ms - variance, base_ms + variance)
        time.sleep_ms(int(delay))
    
    def _jig_cycle(self):
        """执行 JIG 循环"""
        try:
            self._keyboard.press(';')
            self._random_sleep_ms(self._time_press)
            self._keyboard.release(';')
            self._random_sleep_ms(self._time_release)
        except Exception as e:
            print(f"[ERROR] RF4Service._jig_cycle: {e}")
            import sys
            sys.print_exception(e)
    
    def _pull_cycle(self):
        """执行 PULL 循环"""
        try:
            self._keyboard.press(';')
            self._keyboard.press("'")
            self._random_sleep_ms(self._time_press)
            self._keyboard.release("'")
            self._random_sleep_ms(self._time_release)
        except Exception as e:
            print(f"[ERROR] RF4Service._pull_cycle: {e}")
            import sys
            sys.print_exception(e)
    
    def run(self):
        """运行服务主循环（阻塞）"""
        while True:
            try:
                if self._state == RF4State.JIG:
                    self._jig_cycle()
                elif self._state == RF4State.PULL:
                    self._pull_cycle()
                else:
                    time.sleep(2)
            except KeyboardInterrupt:
                print("[INFO] RF4 service stopped")
                break
            except Exception as e:
                print(f"[ERROR] RF4Service.run: {e}")
                import sys
                sys.print_exception(e)
                time.sleep(1)
    
    def set_state(self, state, press_ms=None, release_ms=None):
        """
        设置运行状态
        
        Args:
            state: 状态（RF4State.IDLE/JIG/PULL）
            press_ms: 按压时间（毫秒）
            release_ms: 释放时间（毫秒）
        """
        self._state = state
        if press_ms is not None:
            self._time_press = press_ms
        if release_ms is not None:
            self._time_release = release_ms
    
    def stop(self):
        """停止服务"""
        self._state = RF4State.IDLE
