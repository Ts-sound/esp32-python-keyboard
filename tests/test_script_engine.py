"""
Script Engine Unit Tests

Tests for script storage and basic operations.
"""

import unittest
import sys
import os
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock, call

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

import micropython

from script_engine import ScriptEngine


class TestScriptEngine(unittest.TestCase):
    """Script Engine Test Class"""
    
    def setUp(self):
        """Setup before each test"""
        self.engine = ScriptEngine()
    
    def test_upload_creates_script(self):
        """Test upload creates a new script"""
        result = self.engine.upload("jig", [{"action": "key_press", "key": "a"}], loop=True)
        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "OK")
    
    def test_upload_updates_existing_script(self):
        """Test upload updates an existing script"""
        self.engine.upload("jig", [{"action": "key_press", "key": "a"}], loop=True)
        result = self.engine.upload("jig", [{"action": "key_press", "key": "b"}], loop=False)
        self.assertTrue(result["success"])
        self.assertEqual(self.engine._scripts["jig"]["steps"][0]["key"], "b")
    
    def test_delete_removes_script(self):
        """Test delete removes a script"""
        self.engine.upload("jig", [{"action": "key_press", "key": "a"}], loop=True)
        result = self.engine.delete("jig")
        self.assertTrue(result["success"])
        self.assertNotIn("jig", self.engine._scripts)
    
    def test_delete_nonexistent_fails(self):
        """Test delete fails for nonexistent script"""
        result = self.engine.delete("nonexistent")
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Script not found: nonexistent")
    
    def test_list_returns_script_names(self):
        """Test list returns all script names"""
        self.engine.upload("jig", [], loop=True)
        self.engine.upload("pull", [], loop=False)
        self.engine.upload("custom", [], loop=True)
        result = self.engine.list()
        self.assertTrue(result["success"])
        self.assertEqual(sorted(result["data"]["scripts"]), ["custom", "jig", "pull"])
    
    def test_list_empty_returns_empty_list(self):
        """Test list returns empty list when no scripts"""
        result = self.engine.list()
        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["scripts"], [])
    
    def test_upload_rejects_when_limit_reached(self):
        """Test upload rejects when max scripts limit is reached"""
        for i in range(5):
            self.engine.upload(f"script{i}", [], loop=True)
        result = self.engine.upload("script5", [], loop=True)
        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Script limit reached (max 5)")


class TestScriptEngineExecution(unittest.TestCase):
    """Script Engine Execution Test Class"""

    def setUp(self):
        """Setup before each test"""
        self.engine = ScriptEngine()
        self.keyboard = MagicMock()
        self.keyboard.press = MagicMock()
        self.keyboard.release = MagicMock()
        self.keyboard.release_all = MagicMock()

    def _run_async(self, coro):
        """Helper to run async tests"""
        return asyncio.get_event_loop().run_until_complete(coro)

    @patch('script_engine.asyncio.sleep_ms', new_callable=AsyncMock)
    def test_run_executes_single_step(self, mock_sleep):
        """Test run executes a single step"""
        self.engine.upload("test", [
            {"keys": ["a"], "press_ms": 50, "release_ms": 100}
        ], loop=False, variance_ms=0)

        self._run_async(self.engine.run("test", self.keyboard))

        self.keyboard.press.assert_called_once_with("a")
        self.keyboard.release.assert_called_once_with("a")

    @patch('script_engine.asyncio.sleep_ms', new_callable=AsyncMock)
    def test_run_executes_steps_sequentially(self, mock_sleep):
        """Test run executes multiple steps in order"""
        self.engine.upload("test", [
            {"keys": ["a"], "press_ms": 50, "release_ms": 50},
            {"keys": ["b"], "press_ms": 50, "release_ms": 50},
            {"keys": ["c"], "press_ms": 50, "release_ms": 50}
        ], loop=False, variance_ms=0)

        self._run_async(self.engine.run("test", self.keyboard))

        expected_calls = [call("a"), call("b"), call("c")]
        self.assertEqual(self.keyboard.press.call_args_list, expected_calls)

    @patch('script_engine.asyncio.sleep_ms', new_callable=AsyncMock)
    def test_run_applies_variance_to_timing(self, mock_sleep):
        """Test run applies random variance to press_ms and release_ms"""
        self.engine.upload("test", [
            {"keys": ["a"], "press_ms": 50, "release_ms": 100}
        ], loop=False, variance_ms=10)

        with patch('script_engine.random.uniform') as mock_uniform:
            mock_uniform.side_effect = [45, 105]
            self._run_async(self.engine.run("test", self.keyboard))

        self.assertEqual(mock_sleep.call_count, 2)
        mock_sleep.assert_any_call(45)
        mock_sleep.assert_any_call(105)

    @patch('script_engine.asyncio.sleep_ms', new_callable=AsyncMock)
    def test_run_loop_false_executes_once(self, mock_sleep):
        """Test run with loop=False executes once"""
        self.engine.upload("test", [
            {"keys": ["a"], "press_ms": 50, "release_ms": 50}
        ], loop=False, variance_ms=0)

        self._run_async(self.engine.run("test", self.keyboard))

        self.assertEqual(self.keyboard.press.call_count, 1)

    @patch('script_engine.asyncio.sleep_ms', new_callable=AsyncMock)
    def test_run_loop_int_executes_n_times(self, mock_sleep):
        """Test run with loop=3 executes 3 times"""
        self.engine.upload("test", [
            {"keys": ["a"], "press_ms": 50, "release_ms": 50}
        ], loop=3, variance_ms=0)

        self._run_async(self.engine.run("test", self.keyboard))

        self.assertEqual(self.keyboard.press.call_count, 3)

    @patch('script_engine.asyncio.sleep_ms', new_callable=AsyncMock)
    def test_run_step_variance_overrides_script_variance(self, mock_sleep):
        """Test step-level variance_ms overrides script-level variance_ms"""
        self.engine.upload("test", [
            {"keys": ["a"], "press_ms": 50, "release_ms": 100, "variance_ms": 20}
        ], loop=False, variance_ms=5)

        with patch('script_engine.random.uniform') as mock_uniform:
            mock_uniform.side_effect = [40, 110]
            self._run_async(self.engine.run("test", self.keyboard))

        mock_uniform.assert_any_call(50 - 20, 50 + 20)
        mock_uniform.assert_any_call(100 - 20, 100 + 20)

    @patch('script_engine.asyncio.sleep_ms', new_callable=AsyncMock)
    def test_run_multiple_keys_in_step(self, mock_sleep):
        """Test run handles multiple keys in a single step"""
        self.engine.upload("test", [
            {"keys": ["ctrl", "a"], "press_ms": 50, "release_ms": 50}
        ], loop=False, variance_ms=0)

        self._run_async(self.engine.run("test", self.keyboard))

        expected_press_calls = [call("ctrl"), call("a")]
        expected_release_calls = [call("ctrl"), call("a")]
        self.assertEqual(self.keyboard.press.call_args_list, expected_press_calls)
        self.assertEqual(self.keyboard.release.call_args_list, expected_release_calls)

    @patch('script_engine.asyncio.sleep_ms', new_callable=AsyncMock)
    def test_run_returns_error_for_nonexistent_script(self, mock_sleep):
        """Test run returns error for nonexistent script"""
        result = self._run_async(self.engine.run("nonexistent", self.keyboard))

        self.assertFalse(result["success"])
        self.assertIn("not found", result["message"].lower())

    @patch('script_engine.asyncio.sleep_ms', new_callable=AsyncMock)
    def test_run_uses_default_timing_when_not_specified(self, mock_sleep):
        """Test run uses default press_ms and release_ms when not specified"""
        self.engine.upload("test", [
            {"keys": ["a"]}
        ], loop=False, variance_ms=0)

        self._run_async(self.engine.run("test", self.keyboard))

        mock_sleep.assert_any_call(50)
        self.assertEqual(mock_sleep.call_count, 2)


if __name__ == "__main__":
    unittest.main()