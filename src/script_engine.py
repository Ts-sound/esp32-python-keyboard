"""
Script Engine Module

Manages script storage and basic operations.
"""

import asyncio
import random

from config import MAX_SCRIPTS


DEFAULT_PRESS_MS = 50
DEFAULT_RELEASE_MS = 50


class ScriptEngine:
    """
    Script Storage and Management
    
    Features:
    - Store up to MAX_SCRIPTS scripts
    - Upload, delete, list operations
    - Script format: {name: {steps: [...], loop: bool}}
    """
    
    def __init__(self):
        """Initialize script engine with empty storage"""
        self._scripts = {}
    
    def upload(self, name, steps, loop=False, variance_ms=0):
        """
        Upload or update a script
        
        Args:
            name: Script name
            steps: List of step dictionaries
            loop: Whether script should loop
            variance_ms: Random variance in milliseconds
            
        Returns:
            dict: {success: bool, message: str}
        """
        if name not in self._scripts and len(self._scripts) >= MAX_SCRIPTS:
            return {"success": False, "message": f"Script limit reached (max {MAX_SCRIPTS})"}
        
        self._scripts[name] = {
            "steps": steps,
            "loop": loop,
            "variance_ms": variance_ms
        }
        return {"success": True, "message": "OK"}
    
    def delete(self, name):
        """
        Delete a script
        
        Args:
            name: Script name
            
        Returns:
            dict: {success: bool, message: str}
        """
        if name not in self._scripts:
            return {"success": False, "message": f"Script not found: {name}"}
        
        del self._scripts[name]
        return {"success": True, "message": "OK"}
    
    def list(self):
        """
        List all script names
        
        Returns:
            dict: {success: bool, message: str, data: {scripts: [str]}}
        """
        return {
            "success": True,
            "message": "OK",
            "data": {"scripts": list(self._scripts.keys())}
        }
    
    async def run(self, name, keyboard_device):
        """
        Run a script
        
        Args:
            name: Script name
            keyboard_device: Keyboard device instance
            
        Returns:
            dict: {success: bool, message: str}
        """
        if name not in self._scripts:
            return {"success": False, "message": f"Script not found: {name}"}
        
        script = self._scripts[name]
        steps = script.get("steps", [])
        loop = script.get("loop", False)
        script_variance = script.get("variance_ms", 0)
        
        loop_count = 0
        max_loops = None if loop is True else (loop if isinstance(loop, int) and loop > 0 else 1)
        
        while max_loops is None or loop_count < max_loops:
            for step in steps:
                await self._execute_step(step, keyboard_device, script_variance)
            loop_count += 1
        
        return {"success": True, "message": "OK"}
    
    async def _execute_step(self, step, keyboard_device, script_variance):
        """
        Execute a single step
        
        Args:
            step: Step dictionary with keys, press_ms, release_ms, variance_ms
            keyboard_device: Keyboard device instance
            script_variance: Default variance from script level
        """
        keys = step.get("keys", [])
        press_ms = step.get("press_ms", DEFAULT_PRESS_MS)
        release_ms = step.get("release_ms", DEFAULT_RELEASE_MS)
        variance_ms = step.get("variance_ms", script_variance)
        
        for key in keys:
            keyboard_device.press(key)
        
        await self._random_sleep_ms_async(press_ms, variance_ms)
        
        for key in keys:
            keyboard_device.release(key)
        
        await self._random_sleep_ms_async(release_ms, variance_ms)
    
    async def _random_sleep_ms_async(self, base_ms, variance_ms):
        """
        Random delay (async)
        
        Args:
            base_ms: Base delay time in milliseconds
            variance_ms: Random variance in milliseconds
        """
        delay = int(random.uniform(base_ms - variance_ms, base_ms + variance_ms))
        await asyncio.sleep_ms(delay)