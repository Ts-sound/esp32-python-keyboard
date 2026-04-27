"""
ProtocolParser 单元测试

注意：此测试设计用于在 PC 上使用 CPython 运行。
ESP32 上请手动测试。
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from protocol_parser import ProtocolParser


class TestProtocolParser(unittest.TestCase):
    """ProtocolParser 测试类"""

    def setUp(self):
        self.parser = ProtocolParser()

    def test_parse_valid_keyboard_command(self):
        """测试解析有效的键盘命令"""
        json_str = '{"v":1,"type":"keyboard","action":"press","params":{"keys":["a"]}}'
        result = self.parser.parse(json_str)
        self.assertTrue(result['success'])
        self.assertEqual(result['type'], 'keyboard')
        self.assertEqual(result['action'], 'press')
        self.assertEqual(result['params'], {'keys': ['a']})

    def test_parse_valid_script_command(self):
        """测试解析有效的脚本命令"""
        json_str = '{"v":1,"type":"script","action":"upload","params":{"name":"test"}}'
        result = self.parser.parse(json_str)
        self.assertTrue(result['success'])
        self.assertEqual(result['type'], 'script')
        self.assertEqual(result['action'], 'upload')

    def test_parse_command_without_params(self):
        """测试解析无参数命令"""
        json_str = '{"v":1,"type":"keyboard","action":"release_all"}'
        result = self.parser.parse(json_str)
        self.assertTrue(result['success'])
        self.assertEqual(result['params'], {})

    def test_invalid_json_returns_error(self):
        """测试无效 JSON 返回错误"""
        json_str = 'not valid json'
        result = self.parser.parse(json_str)
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'Invalid JSON')

    def test_missing_field_v_returns_error(self):
        """测试缺少 v 字段返回错误"""
        json_str = '{"type":"keyboard","action":"press"}'
        result = self.parser.parse(json_str)
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'Missing field: v')

    def test_missing_field_type_returns_error(self):
        """测试缺少 type 字段返回错误"""
        json_str = '{"v":1,"action":"press"}'
        result = self.parser.parse(json_str)
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'Missing field: type')

    def test_missing_field_action_returns_error(self):
        """测试缺少 action 字段返回错误"""
        json_str = '{"v":1,"type":"keyboard"}'
        result = self.parser.parse(json_str)
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'Missing field: action')

    def test_unknown_type_returns_error(self):
        """测试未知类型返回错误"""
        json_str = '{"v":1,"type":"unknown","action":"press"}'
        result = self.parser.parse(json_str)
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'Unknown type: unknown')

    def test_unknown_keyboard_action_returns_error(self):
        """测试未知键盘操作返回错误"""
        json_str = '{"v":1,"type":"keyboard","action":"unknown"}'
        result = self.parser.parse(json_str)
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'Unknown action: unknown')

    def test_unknown_script_action_returns_error(self):
        """测试未知脚本操作返回错误"""
        json_str = '{"v":1,"type":"script","action":"unknown"}'
        result = self.parser.parse(json_str)
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'Unknown action: unknown')

    def test_all_keyboard_actions_valid(self):
        """测试所有键盘操作都有效"""
        actions = ['press', 'release', 'release_all', 'type', 'sequence']
        for action in actions:
            json_str = f'{{"v":1,"type":"keyboard","action":"{action}"}}'
            result = self.parser.parse(json_str)
            self.assertTrue(result['success'], f'Action {action} should be valid')

    def test_all_script_actions_valid(self):
        """测试所有脚本操作都有效"""
        actions = ['upload', 'list', 'run', 'pause', 'resume', 'stop', 'delete', 'status']
        for action in actions:
            json_str = f'{{"v":1,"type":"script","action":"{action}"}}'
            result = self.parser.parse(json_str)
            self.assertTrue(result['success'], f'Action {action} should be valid')


if __name__ == "__main__":
    unittest.main()