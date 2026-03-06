"""
消息队列驱动

提供发布/订阅模式的消息队列实现。
支持固定大小缓冲区，防止内存溢出。
"""

from collections import deque


class MessageQueue:
    """
    简单消息队列实现
    
    功能:
    - 发布/订阅模式
    - 固定大小缓冲区（防止内存溢出）
    - 支持超时轮询
    
    使用示例:
        mq = MessageQueue(max_size=10)
        mq.subscribe("wifi/raw", my_callback)
        mq.publish("wifi/raw", "Hello")
        msg = mq.poll(timeout_ms=1000)
    """
    
    def __init__(self, max_size=10):
        """
        初始化消息队列
        
        Args:
            max_size: 队列最大长度（默认 10）
        """
        self._queue = deque((), max_size)
        self._subscribers = {}
    
    def publish(self, topic, msg):
        """
        发布消息到队列
        
        Args:
            topic: 消息主题
            msg: 消息内容
            
        Returns:
            bool: 是否发布成功
        """
        try:
            self._queue.append((topic, msg))
            self._invoke_subscribers(topic, msg)
            return True
        except Exception as e:
            print(f"[ERROR] msg_queue.publish: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def subscribe(self, topic, callback):
        """
        订阅主题
        
        Args:
            topic: 消息主题
            callback: 回调函数，签名为 callback(msg)
            
        Returns:
            bool: 是否订阅成功
        """
        try:
            if topic not in self._subscribers:
                self._subscribers[topic] = []
            self._subscribers[topic].append(callback)
            return True
        except Exception as e:
            print(f"[ERROR] msg_queue.subscribe: {e}")
            import sys
            sys.print_exception(e)
            return False
    
    def poll(self, timeout_ms=0):
        """
        轮询消息（可选超时）
        
        Args:
            timeout_ms: 超时时间（毫秒），0 表示非阻塞
            
        Returns:
            tuple: (topic, msg) 或 None
        """
        try:
            if timeout_ms <= 0:
                if self._queue:
                    return self._queue.popleft()
                return None
            else:
                import time
                start = time.ticks_ms()
                while time.ticks_diff(time.ticks_ms(), start) < timeout_ms:
                    if self._queue:
                        return self._queue.popleft()
                    time.sleep_ms(10)
                return None
        except Exception as e:
            print(f"[ERROR] msg_queue.poll: {e}")
            import sys
            sys.print_exception(e)
            return None
    
    def _invoke_subscribers(self, topic, msg):
        """
        调用订阅者回调
        
        Args:
            topic: 消息主题
            msg: 消息内容
        """
        if topic in self._subscribers:
            for callback in self._subscribers[topic]:
                try:
                    callback(msg)
                except Exception as e:
                    print(f"[ERROR] msg_queue.callback: {e}")
                    import sys
                    sys.print_exception(e)
        
        if "*" in self._subscribers:
            for callback in self._subscribers["*"]:
                try:
                    callback(msg)
                except Exception as e:
                    print(f"[ERROR] msg_queue.callback: {e}")
                    import sys
                    sys.print_exception(e)
