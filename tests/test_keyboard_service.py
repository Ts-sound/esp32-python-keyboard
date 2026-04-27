"""
KeyboardService 单元测试

注意：此测试设计用于在 PC 上使用 CPython 运行。
ESP32 上请手动测试。
"""

import unittest
from unittest.mock import Mock, MagicMock, call, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from keyboard_service import KeyboardService


class TestKeyboardService(unittest.TestCase):
    """KeyboardService 测试类"""

    def setUp(self):
        """测试前准备"""
        self.keyboard_device = Mock()
        self.script_engine = Mock()
        self.msg_queue = Mock()
        self.service = KeyboardService(
            keyboard_device=self.keyboard_device,
            script_engine=self.script_engine,
            msg_queue=self.msg_queue
        )

    def test_handle_command_invalid_json(self):
        """测试无效 JSON 返回错误"""
        result = self.service.handle_command("not valid json")
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'Invalid JSON')

    def test_handle_command_missing_fields(self):
        """测试缺少必要字段返回错误"""
        result = self.service.handle_command('{}')
        self.assertFalse(result['success'])

    def test_handle_command_unknown_type(self):
        """测试未知类型返回错误"""
        result = self.service.handle_command('{"v":1,"type":"unknown","action":"test"}')
        self.assertFalse(result['success'])
        self.assertIn('Unknown type', result['message'])

    # ========== Keyboard Press ==========

    def test_keyboard_press_single_key(self):
        """测试按下单个键"""
        result = self.service.handle_command(
            '{"v":1,"type":"keyboard","action":"press","params":{"keys":["a"]}}'
        )
        self.assertTrue(result['success'])
        self.keyboard_device.press.assert_called_once_with('a')

    def test_keyboard_press_multiple_keys(self):
        """测试按下多个键"""
        result = self.service.handle_command(
            '{"v":1,"type":"keyboard","action":"press","params":{"keys":["ctrl","shift","a"]}}'
        )
        self.assertTrue(result['success'])
        self.keyboard_device.press.assert_has_calls([
            call('ctrl'),
            call('shift'),
            call('a')
        ])

    def test_keyboard_press_missing_keys(self):
        """测试 press 缺少 keys 参数"""
        result = self.service.handle_command(
            '{"v":1,"type":"keyboard","action":"press","params":{}}'
        )
        self.assertFalse(result['success'])

    # ========== Keyboard Release ==========

    def test_keyboard_release_single_key(self):
        """测试释放单个键"""
        result = self.service.handle_command(
            '{"v":1,"type":"keyboard","action":"release","params":{"keys":["a"]}}'
        )
        self.assertTrue(result['success'])
        self.keyboard_device.release.assert_called_once_with('a')

    def test_keyboard_release_multiple_keys(self):
        """测试释放多个键"""
        result = self.service.handle_command(
            '{"v":1,"type":"keyboard","action":"release","params":{"keys":["ctrl","shift"]}}'
        )
        self.assertTrue(result['success'])
        self.keyboard_device.release.assert_has_calls([
            call('ctrl'),
            call('shift')
        ])

    # ========== Keyboard Release All ==========

    def test_keyboard_release_all(self):
        """测试释放所有键"""
        result = self.service.handle_command(
            '{"v":1,"type":"keyboard","action":"release_all"}'
        )
        self.assertTrue(result['success'])
        self.keyboard_device.release_all.assert_called_once()

    # ========== Keyboard Type ==========

    def test_keyboard_type_text(self):
        """测试输入文本"""
        with patch('keyboard_service.time') as mock_time:
            result = self.service.handle_command(
                '{"v":1,"type":"keyboard","action":"type","params":{"text":"hello"}}'
            )
            self.assertTrue(result['success'])
            self.keyboard_device.send_string.assert_called_once_with('hello')

    def test_keyboard_type_with_delay(self):
        """测试输入文本带延迟"""
        with patch('keyboard_service.time') as mock_time:
            result = self.service.handle_command(
                '{"v":1,"type":"keyboard","action":"type","params":{"text":"hi","delay_ms":100}}'
            )
            self.assertTrue(result['success'])
            mock_time.sleep_ms.assert_called()

    def test_keyboard_type_missing_text(self):
        """测试 type 缺少 text 参数"""
        result = self.service.handle_command(
            '{"v":1,"type":"keyboard","action":"type","params":{}}'
        )
        self.assertFalse(result['success'])

    # ========== Keyboard Sequence ==========

    def test_keyboard_sequence_single_step(self):
        """测试执行单步序列"""
        with patch('keyboard_service.time') as mock_time:
            mock_time.sleep_ms = Mock()
            result = self.service.handle_command(
                '{"v":1,"type":"keyboard","action":"sequence","params":{"steps":[{"keys":["a"]}]}}'
            )
            self.assertTrue(result['success'])
            self.keyboard_device.press.assert_called_with('a')
            self.keyboard_device.release.assert_called_with('a')

    def test_keyboard_sequence_multiple_steps(self):
        """测试执行多步序列"""
        with patch('keyboard_service.time') as mock_time:
            mock_time.sleep_ms = Mock()
            result = self.service.handle_command(
                '{"v":1,"type":"keyboard","action":"sequence","params":{"steps":[{"keys":["a"]},{"keys":["b"]}]}}'
            )
            self.assertTrue(result['success'])
            self.assertEqual(self.keyboard_device.press.call_count, 2)
            self.assertEqual(self.keyboard_device.release.call_count, 2)

    def test_keyboard_sequence_with_custom_timing(self):
        """测试自定义时间的序列"""
        with patch('keyboard_service.time') as mock_time:
            mock_time.sleep_ms = Mock()
            result = self.service.handle_command(
                '{"v":1,"type":"keyboard","action":"sequence","params":{"steps":[{"keys":["a"],"press_ms":100,"release_ms":200}]}}'
            )
            self.assertTrue(result['success'])
            mock_time.sleep_ms.assert_called()

    def test_keyboard_sequence_with_loop(self):
        """测试循环序列"""
        with patch('keyboard_service.time') as mock_time:
            mock_time.sleep_ms = Mock()
            result = self.service.handle_command(
                '{"v":1,"type":"keyboard","action":"sequence","params":{"steps":[{"keys":["a"]}],"loop":3}}'
            )
            self.assertTrue(result['success'])
            self.assertEqual(self.keyboard_device.press.call_count, 3)

    @unittest.skip("Infinite loop cannot be tested in unit tests")
    def test_keyboard_sequence_with_infinite_loop_true(self):
        """测试无限循环 (loop: true) - 跳过因为无法停止"""
        with patch('keyboard_service.time') as mock_time:
            mock_time.sleep_ms = Mock()
            result = self.service.handle_command(
                '{"v":1,"type":"keyboard","action":"sequence","params":{"steps":[{"keys":["a"]}],"loop":true}}'
            )
            self.assertTrue(result['success'])

    def test_keyboard_sequence_missing_steps(self):
        """测试 sequence 缺少 steps 参数"""
        result = self.service.handle_command(
            '{"v":1,"type":"keyboard","action":"sequence","params":{}}'
        )
        self.assertFalse(result['success'])

    # ========== Script Upload ==========

    def test_script_upload(self):
        """测试上传脚本"""
        self.script_engine.upload.return_value = {"success": True, "message": "OK"}
        result = self.service.handle_command(
            '{"v":1,"type":"script","action":"upload","params":{"name":"test","steps":[{"keys":["a"]}]}}'
        )
        self.assertTrue(result['success'])
        self.script_engine.upload.assert_called_once_with(
            name='test',
            steps=[{'keys': ['a'], 'press_ms': 50, 'release_ms': 50, 'variance_ms': 0}],
            loop=False,
            variance_ms=0
        )

    def test_script_upload_with_options(self):
        """测试上传脚本带选项"""
        self.script_engine.upload.return_value = {"success": True, "message": "OK"}
        result = self.service.handle_command(
            '{"v":1,"type":"script","action":"upload","params":{"name":"test","steps":[{"keys":["a"]}],"loop":true,"variance_ms":10}}'
        )
        self.assertTrue(result['success'])
        self.script_engine.upload.assert_called_once_with(
            name='test',
            steps=[{'keys': ['a'], 'press_ms': 50, 'release_ms': 50, 'variance_ms': 10}],
            loop=True,
            variance_ms=10
        )

    # ========== Script Delete ==========

    def test_script_delete(self):
        """测试删除脚本"""
        self.script_engine.delete.return_value = {"success": True, "message": "OK"}
        result = self.service.handle_command(
            '{"v":1,"type":"script","action":"delete","params":{"name":"test"}}'
        )
        self.assertTrue(result['success'])
        self.script_engine.delete.assert_called_once_with(name='test')

    # ========== Script List ==========

    def test_script_list(self):
        """测试列出脚本"""
        self.script_engine.list.return_value = {"success": True, "data": {"scripts": ["a", "b"]}}
        result = self.service.handle_command(
            '{"v":1,"type":"script","action":"list"}'
        )
        self.assertTrue(result['success'])
        self.script_engine.list.assert_called_once()

    # ========== Script Status ==========

    def test_script_status(self):
        """测试获取脚本状态"""
        self.script_engine.status.return_value = {"success": True, "data": {"running": False}}
        result = self.service.handle_command(
            '{"v":1,"type":"script","action":"status"}'
        )
        self.assertTrue(result['success'])
        self.script_engine.status.assert_called_once()

    # ========== Script Pause/Resume/Stop ==========

    def test_script_pause(self):
        """测试暂停脚本"""
        self.script_engine.pause.return_value = {"success": True}
        result = self.service.handle_command(
            '{"v":1,"type":"script","action":"pause"}'
        )
        self.assertTrue(result['success'])
        self.script_engine.pause.assert_called_once()

    def test_script_resume(self):
        """测试恢复脚本"""
        self.script_engine.resume.return_value = {"success": True}
        result = self.service.handle_command(
            '{"v":1,"type":"script","action":"resume"}'
        )
        self.assertTrue(result['success'])
        self.script_engine.resume.assert_called_once()

    def test_script_stop(self):
        """测试停止脚本"""
        self.script_engine.stop.return_value = {"success": True}
        result = self.service.handle_command(
            '{"v":1,"type":"script","action":"stop"}'
        )
        self.assertTrue(result['success'])
        self.script_engine.stop.assert_called_once()

    # ========== Script Run ==========

    def test_script_run_queues_script(self):
        """测试脚本 run 调用 queue_run"""
        self.script_engine.queue_run.return_value = {"success": True, "message": "OK"}
        result = self.service.handle_command(
            '{"v":1,"type":"script","action":"run","params":{"name":"test"}}'
        )
        self.assertTrue(result['success'])
        self.script_engine.queue_run.assert_called_once_with(name="test")

    # ========== Message Queue Integration ==========

    def test_handle_raw_message_publishes_response(self):
        """测试原始消息处理后发布响应"""
        self.service.handle_command = Mock(return_value={"success": True, "message": "OK"})
        self.service._handle_raw_message('{"v":1,"type":"keyboard","action":"release_all"}')
        self.service._msg_queue.publish.assert_called_once_with(
            "keyboard/response",
            {"success": True, "message": "OK"}
        )

    def test_handle_raw_message_invalid_json(self):
        """测试无效 JSON 发布错误响应"""
        self.service._handle_raw_message('invalid')
        self.service._msg_queue.publish.assert_called_once()
        call_args = self.service._msg_queue.publish.call_args
        self.assertEqual(call_args[0][0], "keyboard/response")
        self.assertFalse(call_args[0][1]['success'])


if __name__ == "__main__":
    unittest.main()