"""
消息队列单元测试

注意：此测试设计用于在 PC 上使用 CPython 运行。
ESP32 上请手动测试。
"""

import unittest
from unittest.mock import Mock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src/drivers'))

from msg_queue import MessageQueue


class TestMessageQueue(unittest.TestCase):
    """消息队列测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.mq = MessageQueue(max_size=5)
    
    def test_publish_simple(self):
        """测试简单发布"""
        result = self.mq.publish("test", "hello")
        self.assertTrue(result)
    
    def test_subscribe_and_callback(self):
        """测试订阅和回调"""
        callback = Mock()
        self.mq.subscribe("test", callback)
        self.mq.publish("test", "hello")
        callback.assert_called_once_with("hello")
    
    def test_poll_non_blocking(self):
        """测试非阻塞轮询"""
        self.mq.publish("test", "msg1")
        msg = self.mq.poll(timeout_ms=0)
        self.assertEqual(msg, ("test", "msg1"))
    
    def test_poll_empty(self):
        """测试空队列轮询"""
        msg = self.mq.poll(timeout_ms=0)
        self.assertIsNone(msg)
    
    def test_queue_max_size(self):
        """测试队列最大大小"""
        for i in range(10):
            self.mq.publish("test", f"msg{i}")
        self.assertEqual(len(self.mq._queue), 5)
    
    def test_wildcard_subscribe(self):
        """测试通配符订阅"""
        callback = Mock()
        self.mq.subscribe("*", callback)
        self.mq.publish("any_topic", "hello")
        callback.assert_called_once_with("hello")
    
    def test_multiple_subscribers(self):
        """测试多个订阅者"""
        callback1 = Mock()
        callback2 = Mock()
        self.mq.subscribe("test", callback1)
        self.mq.subscribe("test", callback2)
        self.mq.publish("test", "hello")
        callback1.assert_called_once_with("hello")
        callback2.assert_called_once_with("hello")


if __name__ == "__main__":
    unittest.main()
