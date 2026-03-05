"""
HID 映射表单元测试

注意：此测试设计用于在 PC 上使用 CPython 运行。
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from hid_mapper import HID_KEYMAP, HID_MODIFIERS, get_hid_code, get_modifier_code, parse_key_string


class TestHIDMapper(unittest.TestCase):
    """HID 映射表测试类"""
    
    def test_all_lowercase_letters(self):
        """测试所有小写字母映射"""
        for c in 'abcdefghijklmnopqrstuvwxyz':
            code = get_hid_code(c)
            self.assertIsNotNone(code, f"Missing mapping for '{c}'")
            self.assertIsInstance(code, int)
    
    def test_all_digits(self):
        """测试所有数字映射"""
        for c in '0123456789':
            code = get_hid_code(c)
            self.assertIsNotNone(code, f"Missing mapping for '{c}'")
    
    def test_special_keys(self):
        """测试特殊按键"""
        special_keys = ['enter', 'escape', 'backspace', 'tab', 'space', 'capslock']
        for key in special_keys:
            code = get_hid_code(key)
            self.assertIsNotNone(code, f"Missing mapping for '{key}'")
    
    def test_function_keys(self):
        """测试功能键"""
        for i in range(1, 13):
            key = f'f{i}'
            code = get_hid_code(key)
            self.assertIsNotNone(code, f"Missing mapping for '{key}'")
    
    def test_modifier_codes(self):
        """测试修饰键"""
        modifiers = ['left_control', 'left_shift', 'left_alt', 'left_gui',
                     'right_control', 'right_shift', 'right_alt', 'right_gui']
        for mod in modifiers:
            code = get_modifier_code(mod)
            self.assertNotEqual(code, 0, f"Missing modifier '{mod}'")
    
    def test_parse_key_string_simple(self):
        """测试解析简单按键"""
        code, mod = parse_key_string("a")
        self.assertEqual(code, HID_KEYMAP['a'])
        self.assertEqual(mod, 0)
    
    def test_parse_key_string_shift(self):
        """测试解析带 Shift 的按键"""
        code, mod = parse_key_string("Shift+A")
        self.assertEqual(code, HID_KEYMAP['a'])
        self.assertNotEqual(mod, 0)
    
    def test_parse_key_string_ctrl(self):
        """测试解析带 Ctrl 的按键"""
        code, mod = parse_key_string("Ctrl+S")
        self.assertEqual(code, HID_KEYMAP['s'])
        self.assertNotEqual(mod, 0)
    
    def test_unknown_key(self):
        """测试未知按键"""
        code = get_hid_code("unknown_key_xyz")
        self.assertIsNone(code)


if __name__ == "__main__":
    unittest.main()
