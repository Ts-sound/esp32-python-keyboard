"""
键盘设备单元测试

注意：此测试设计用于在 PC 上使用 CPython 运行。
ESP32 上请手动测试。
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src/devices'))

from hid_mapper import HID_KEYMAP


class TestKeyboardDevice(unittest.TestCase):
    """键盘设备测试类（Mock 测试）"""
    
    def test_hid_keymap_letters(self):
        """测试字母键映射"""
        for c in 'abcdefghijklmnopqrstuvwxyz':
            self.assertIn(c, HID_KEYMAP)
            self.assertIsInstance(HID_KEYMAP[c], int)
    
    def test_hid_keymap_digits(self):
        """测试数字键映射"""
        for c in '0123456789':
            self.assertIn(c, HID_KEYMAP)
    
    def test_hid_keymap_special(self):
        """测试特殊按键"""
        special_keys = ['enter', 'escape', 'backspace', 'tab', 'space']
        for key in special_keys:
            self.assertIn(key, HID_KEYMAP)
    
    def test_hid_keymap_punctuation(self):
        """测试标点符号"""
        punctuations = [';', "'", ',', '.', '/', '-', '[', ']', '\\\\', '#', '`']
        for p in punctuations:
            self.assertIn(p, HID_KEYMAP)
    
    def test_hid_keymap_function(self):
        """测试功能键"""
        for i in range(1, 13):
            key = f'f{i}'
            self.assertIn(key, HID_KEYMAP)
    
    def test_hid_keymap_arrows(self):
        """测试方向键"""
        arrows = ['up', 'down', 'left', 'right']
        for a in arrows:
            self.assertIn(a, HID_KEYMAP)
    
    def test_key_codes_unique(self):
        """测试键码唯一性"""
        values = list(HID_KEYMAP.values())
        self.assertEqual(len(values), len(set(values)), "Duplicate key codes found")


if __name__ == "__main__":
    unittest.main()
