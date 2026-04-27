"""
Script Engine Unit Tests

Tests for script storage and basic operations.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

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


if __name__ == "__main__":
    unittest.main()