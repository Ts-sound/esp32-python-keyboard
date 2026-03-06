"""
Message Queue Driver

Provides publish/subscribe pattern message queue implementation.
Supports fixed-size buffer to prevent memory overflow.
"""

from collections import deque


class MessageQueue:
    """
    Simple Message Queue Implementation
    
    Features:
    - Publish/subscribe pattern
    - Fixed-size buffer (prevents memory overflow)
    - Timeout polling support
    
    Usage Example:
        mq = MessageQueue(max_size=10)
        mq.subscribe("wifi/raw", my_callback)
        mq.publish("wifi/raw", "Hello")
        msg = mq.poll(timeout_ms=1000)
    """
    
    def __init__(self, max_size=10):
        """
        Initialize message queue
        
        Args:
            max_size: Maximum queue size (default 10)
        """
        self._queue = deque((), max_size)
        self._subscribers = {}
    
    def publish(self, topic, msg):
        """
        Publish message to queue
        
        Args:
            topic: Message topic
            msg: Message content
            
        Returns:
            bool: Success status
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
        Subscribe to topic
        
        Args:
            topic: Message topic
            callback: Callback function with signature callback(msg)
            
        Returns:
            bool: Success status
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
        Poll message (optional timeout)
        
        Args:
            timeout_ms: Timeout in milliseconds, 0 for non-blocking
            
        Returns:
            tuple: (topic, msg) or None
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
        Invoke subscriber callbacks
        
        Args:
            topic: Message topic
            msg: Message content
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
