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
    
    IDLE = 0
    RUNNING = 1
    PAUSED = 2
    
    def __init__(self):
        """Initialize script engine with empty storage"""
        self._scripts = {}
        self._state = self.IDLE
        self._current_script = None
        self._current_step = 0
        self._loop_count = 0
        self._total_steps = 0
        self._max_loops = 1
        self._pause_event = None
        self._stop_flag = False
    
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
        
        self._state = self.RUNNING
        self._current_script = name
        self._total_steps = len(steps)
        self._loop_count = 0
        self._max_loops = None if loop is True else (loop if isinstance(loop, int) and loop > 0 else 1)
        self._pause_event = asyncio.Event()
        self._pause_event.set()
        self._stop_flag = False
        
        while self._max_loops is None or self._loop_count < self._max_loops:
            self._current_step = 0
            for step in steps:
                if self._stop_flag:
                    self._state = self.IDLE
                    return {"success": True, "message": "OK"}
                await self._pause_event.wait()
                if self._stop_flag:
                    self._state = self.IDLE
                    return {"success": True, "message": "OK"}
                await self._execute_step(step, keyboard_device, script_variance)
                self._current_step += 1
            self._loop_count += 1
        
        self._state = self.IDLE
        return {"success": True, "message": "OK"}
    
    def pause(self):
        """
        Pause current execution
        
        Returns:
            dict: {success: bool, message: str}
        """
        if self._state != self.RUNNING:
            return {"success": False, "message": "No script running"}
        
        self._state = self.PAUSED
        if self._pause_event:
            self._pause_event.clear()
        return {"success": True, "message": "OK"}
    
    def resume(self):
        """
        Resume from paused state
        
        Returns:
            dict: {success: bool, message: str}
        """
        if self._state != self.PAUSED:
            return {"success": False, "message": "Script not paused"}
        
        self._state = self.RUNNING
        if self._pause_event:
            self._pause_event.set()
        return {"success": True, "message": "OK"}
    
    def stop(self):
        """
        Stop execution and clear state
        
        Returns:
            dict: {success: bool, message: str}
        """
        if self._state == self.IDLE:
            return {"success": False, "message": "No script running"}
        
        self._stop_flag = True
        if self._pause_event:
            self._pause_event.set()
        return {"success": True, "message": "OK"}
    
    def status(self):
        """
        Get current execution status
        
        Returns:
            dict: {success: bool, message: str, data: {...}}
        """
        running = self._state == self.RUNNING
        paused = self._state == self.PAUSED
        
        max_loops_display = True if self._max_loops is None else self._max_loops
        
        return {
            "success": True,
            "message": "OK",
            "data": {
                "running": running,
                "paused": paused,
                "script": self._current_script,
                "step": self._current_step,
                "total_steps": self._total_steps,
                "loop_count": self._loop_count,
                "max_loops": max_loops_display
            }
        }
    
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