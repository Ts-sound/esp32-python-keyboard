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
        action_params = {
            'press': '{"keys":["a"]}',
            'release': '{"keys":["a"]}',
            'release_all': '{}',
            'type': '{"text":"hi"}',
            'sequence': '{"steps":[{"keys":["a"]}]}'
        }
        for action in action_params:
            json_str = f'{{"v":1,"type":"keyboard","action":"{action}","params":{action_params[action]}}}'
            result = self.parser.parse(json_str)
            self.assertTrue(result['success'], f'Action {action} should be valid')

    def test_all_script_actions_valid(self):
        """测试所有脚本操作都有效"""
        actions = ['upload', 'list', 'run', 'pause', 'resume', 'stop', 'delete', 'status']
        for action in actions:
            json_str = f'{{"v":1,"type":"script","action":"{action}"}}'
            result = self.parser.parse(json_str)
            self.assertTrue(result['success'], f'Action {action} should be valid')


# ========== Keyboard Press/Release Validation ==========

    def test_press_requires_keys(self):
        """测试 press 命令需要 keys 参数"""
        json_str = '{"v":1,"type":"keyboard","action":"press","params":{}}'
        result = self.parser.parse(json_str)
        self.assertFalse(result['success'])
        self.assertIn('keys', result['message'])

    def test_press_keys_must_be_array(self):
        """测试 press keys 必须是数组"""
        json_str = '{"v":1,"type":"keyboard","action":"press","params":{"keys":"a"}}'
        result = self.parser.parse(json_str)
        self.assertFalse(result['success'])
        self.assertIn('keys', result['message'])

    def test_press_keys_must_be_non_empty(self):
        """测试 press keys 不能为空数组"""
        json_str = '{"v":1,"type":"keyboard","action":"press","params":{"keys":[]}}'
        result = self.parser.parse(json_str)
        self.assertFalse(result['success'])
        self.assertIn('keys', result['message'])

    def test_press_valid_keys(self):
        """测试有效的 press keys"""
        json_str = '{"v":1,"type":"keyboard","action":"press","params":{"keys":["ctrl","s"]}}'
        result = self.parser.parse(json_str)
        self.assertTrue(result['success'])
        self.assertEqual(result['params']['keys'], ['ctrl', 's'])

    def test_release_requires_keys(self):
        """测试 release 命令需要 keys 参数"""
        json_str = '{"v":1,"type":"keyboard","action":"release","params":{}}'
        result = self.parser.parse(json_str)
        self.assertFalse(result['success'])
        self.assertIn('keys', result['message'])

    def test_release_valid_keys(self):
        """测试有效的 release keys"""
        json_str = '{"v":1,"type":"keyboard","action":"release","params":{"keys":["a"]}}'
        result = self.parser.parse(json_str)
        self.assertTrue(result['success'])
        self.assertEqual(result['params']['keys'], ['a'])

    def test_release_all_no_params_required(self):
        """测试 release_all 不需要参数"""
        json_str = '{"v":1,"type":"keyboard","action":"release_all"}'
        result = self.parser.parse(json_str)
        self.assertTrue(result['success'])

    # ========== Keyboard Type Validation ==========

    def test_type_requires_text(self):
        """测试 type 命令需要 text 参数"""
        json_str = '{"v":1,"type":"keyboard","action":"type","params":{}}'
        result = self.parser.parse(json_str)
        self.assertFalse(result['success'])
        self.assertIn('text', result['message'])

    def test_type_text_must_be_string(self):
        """测试 type text 必须是字符串"""
        json_str = '{"v":1,"type":"keyboard","action":"type","params":{"text":123}}'
        result = self.parser.parse(json_str)
        self.assertFalse(result['success'])
        self.assertIn('text', result['message'])

    def test_type_valid_params(self):
        """测试有效的 type 参数"""
        json_str = '{"v":1,"type":"keyboard","action":"type","params":{"text":"Hello","delay_ms":50}}'
        result = self.parser.parse(json_str)
        self.assertTrue(result['success'])
        self.assertEqual(result['params']['text'], 'Hello')
        self.assertEqual(result['params']['delay_ms'], 50)

    def test_type_delay_ms_defaults_to_50(self):
        """测试 type delay_ms 默认值为 50"""
        json_str = '{"v":1,"type":"keyboard","action":"type","params":{"text":"Hi"}}'
        result = self.parser.parse(json_str)
        self.assertTrue(result['success'])
        self.assertEqual(result['params']['delay_ms'], 50)

    # ========== Keyboard Sequence Validation ==========

    def test_sequence_requires_steps(self):
        """测试 sequence 命令需要 steps 参数"""
        json_str = '{"v":1,"type":"keyboard","action":"sequence","params":{}}'
        result = self.parser.parse(json_str)
        self.assertFalse(result['success'])
        self.assertIn('steps', result['message'])

    def test_sequence_steps_must_be_array(self):
        """测试 sequence steps 必须是数组"""
        json_str = '{"v":1,"type":"keyboard","action":"sequence","params":{"steps":"invalid"}}'
        result = self.parser.parse(json_str)
        self.assertFalse(result['success'])
        self.assertIn('steps', result['message'])

    def test_sequence_steps_must_be_non_empty(self):
        """测试 sequence steps 不能为空数组"""
        json_str = '{"v":1,"type":"keyboard","action":"sequence","params":{"steps":[]}}'
        result = self.parser.parse(json_str)
        self.assertFalse(result['success'])
        self.assertIn('steps', result['message'])

    def test_sequence_step_requires_keys(self):
        """测试 sequence step 需要 keys"""
        json_str = '{"v":1,"type":"keyboard","action":"sequence","params":{"steps":[{}]}}'
        result = self.parser.parse(json_str)
        self.assertFalse(result['success'])
        self.assertIn('keys', result['message'])

    def test_sequence_valid_params(self):
        """测试有效的 sequence 参数"""
        json_str = '{"v":1,"type":"keyboard","action":"sequence","params":{"steps":[{"keys":["a"]}],"loop":true,"variance_ms":10}}'
        result = self.parser.parse(json_str)
        self.assertTrue(result['success'])
        self.assertEqual(result['params']['steps'][0]['keys'], ['a'])
        self.assertEqual(result['params']['loop'], True)
        self.assertEqual(result['params']['variance_ms'], 10)

    def test_sequence_loop_defaults_to_false(self):
        """测试 sequence loop 默认为 false"""
        json_str = '{"v":1,"type":"keyboard","action":"sequence","params":{"steps":[{"keys":["a"]}]}}'
        result = self.parser.parse(json_str)
        self.assertTrue(result['success'])
        self.assertEqual(result['params']['loop'], False)

    def test_sequence_variance_ms_defaults_to_0(self):
        """测试 sequence variance_ms 默认为 0"""
        json_str = '{"v":1,"type":"keyboard","action":"sequence","params":{"steps":[{"keys":["a"]}]}}'
        result = self.parser.parse(json_str)
        self.assertTrue(result['success'])
        self.assertEqual(result['params']['variance_ms'], 0)

    def test_sequence_step_defaults_press_release_ms(self):
        """测试 sequence step 默认 press_ms 和 release_ms"""
        json_str = '{"v":1,"type":"keyboard","action":"sequence","params":{"steps":[{"keys":["a"]}]}}'
        result = self.parser.parse(json_str)
        self.assertTrue(result['success'])
        step = result['params']['steps'][0]
        self.assertEqual(step['press_ms'], 50)
        self.assertEqual(step['release_ms'], 50)

    def test_sequence_loop_can_be_int(self):
        """测试 sequence loop 可以是整数"""
        json_str = '{"v":1,"type":"keyboard","action":"sequence","params":{"steps":[{"keys":["a"]}],"loop":3}}'
        result = self.parser.parse(json_str)
        self.assertTrue(result['success'])
        self.assertEqual(result['params']['loop'], 3)

    def test_sequence_step_inherits_variance_ms(self):
        """测试 sequence step 继承上级 variance_ms"""
        json_str = '{"v":1,"type":"keyboard","action":"sequence","params":{"steps":[{"keys":["a"]}],"variance_ms":10}}'
        result = self.parser.parse(json_str)
        self.assertTrue(result['success'])
        step = result['params']['steps'][0]
        self.assertEqual(step['variance_ms'], 10)

    def test_sequence_step_can_override_variance_ms(self):
        """测试 sequence step 可以覆盖 variance_ms"""
        json_str = '{"v":1,"type":"keyboard","action":"sequence","params":{"steps":[{"keys":["a"],"variance_ms":5}],"variance_ms":10}}'
        result = self.parser.parse(json_str)
        self.assertTrue(result['success'])
        step = result['params']['steps'][0]
        self.assertEqual(step['variance_ms'], 5)

    def test_sequence_multiple_steps(self):
        """测试 sequence 多个步骤"""
        json_str = '{"v":1,"type":"keyboard","action":"sequence","params":{"steps":[{"keys":["a"]},{"keys":["b"]}],"variance_ms":20}}'
        result = self.parser.parse(json_str)
        self.assertTrue(result['success'])
        steps = result['params']['steps']
        self.assertEqual(len(steps), 2)
        self.assertEqual(steps[0]['keys'], ['a'])
        self.assertEqual(steps[1]['keys'], ['b'])
        self.assertEqual(steps[0]['variance_ms'], 20)
        self.assertEqual(steps[1]['variance_ms'], 20)


if __name__ == "__main__":
    unittest.main()