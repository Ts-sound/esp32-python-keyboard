"""
Keyboard Service

Handles JSON commands from WiFi and dispatches to KeyboardDevice or ScriptEngine.
"""

import time
import random

from protocol_parser import ProtocolParser


DEFAULT_PRESS_MS = 50
DEFAULT_RELEASE_MS = 50


class KeyboardService:
    """
    Keyboard Service Class
    
    Receives JSON commands from WiFi and dispatches to appropriate handlers.
    """
    
    def __init__(self, keyboard_device, script_engine, msg_queue):
        """
        Initialize keyboard service
        
        Args:
            keyboard_device: KeyboardDevice instance
            script_engine: ScriptEngine instance
            msg_queue: MessageQueue instance
        """
        self._keyboard = keyboard_device
        self._script_engine = script_engine
        self._parser = ProtocolParser()
        self._msg_queue = msg_queue
        
        msg_queue.subscribe("wifi/raw", self._handle_raw_message)
    
    def _handle_raw_message(self, raw_msg):
        """
        Handle raw message from wifi/raw topic
        
        Args:
            raw_msg: Raw JSON string
        """
        response = self.handle_command(raw_msg)
        self._msg_queue.publish("keyboard/response", response)
    
    def handle_command(self, raw_msg):
        """
        Handle JSON command
        
        Args:
            raw_msg: Raw JSON string
            
        Returns:
            dict: Response with success, message, and optional data
        """
        result = self._parser.parse(raw_msg)
        if not result["success"]:
            return result
        
        cmd_type = result["type"]
        action = result["action"]
        params = result["params"]
        
        if cmd_type == "keyboard":
            return self._handle_keyboard(action, params)
        elif cmd_type == "script":
            return self._handle_script(action, params)
        
        return {"success": False, "message": f"Unknown type: {cmd_type}"}
    
    def _handle_keyboard(self, action, params):
        """
        Handle keyboard action
        
        Args:
            action: Keyboard action (press, release, release_all, type, sequence)
            params: Action parameters
            
        Returns:
            dict: Response
        """
        if action == "press":
            return self._do_press(params)
        elif action == "release":
            return self._do_release(params)
        elif action == "release_all":
            return self._do_release_all(params)
        elif action == "type":
            return self._do_type(params)
        elif action == "sequence":
            return self._do_sequence(params)
        
        return {"success": False, "message": f"Unknown keyboard action: {action}"}
    
    def _do_press(self, params):
        """
        Execute press action
        
        Args:
            params: {keys: [...]}
            
        Returns:
            dict: Response
        """
        keys = params["keys"]
        for key in keys:
            self._keyboard.press(key)
        return {"success": True, "message": "OK"}
    
    def _do_release(self, params):
        """
        Execute release action
        
        Args:
            params: {keys: [...]}
            
        Returns:
            dict: Response
        """
        keys = params["keys"]
        for key in keys:
            self._keyboard.release(key)
        return {"success": True, "message": "OK"}
    
    def _do_release_all(self, params):
        """
        Execute release_all action
        
        Args:
            params: {} (ignored)
            
        Returns:
            dict: Response
        """
        self._keyboard.release_all()
        return {"success": True, "message": "OK"}
    
    def _do_type(self, params):
        """
        Execute type action
        
        Args:
            params: {text: str, delay_ms: int}
            
        Returns:
            dict: Response
        """
        text = params["text"]
        delay_ms = params.get("delay_ms", 50)
        
        self._keyboard.send_string(text)
        time.sleep_ms(delay_ms)
        
        return {"success": True, "message": "OK"}
    
    def _do_sequence(self, params):
        """
        Execute sequence action (immediate execution, no storage)
        
        Args:
            params: {steps: [...], loop: bool/int, variance_ms: int}
            
        Returns:
            dict: Response
        """
        steps = params["steps"]
        loop = params.get("loop", False)
        variance_ms = params.get("variance_ms", 0)
        
        max_loops = None if loop is True else (loop if isinstance(loop, int) and loop > 0 else 1)
        loop_count = 0
        
        while max_loops is None or loop_count < max_loops:
            for step in steps:
                self._execute_step(step, variance_ms)
            loop_count += 1
        
        return {"success": True, "message": "OK"}
    
    def _execute_step(self, step, default_variance):
        """
        Execute a single sequence step
        
        Args:
            step: {keys: [...], press_ms: int, release_ms: int, variance_ms: int}
            default_variance: Default variance from sequence level
        """
        keys = step.get("keys", [])
        press_ms = step.get("press_ms", DEFAULT_PRESS_MS)
        release_ms = step.get("release_ms", DEFAULT_RELEASE_MS)
        variance = step.get("variance_ms", default_variance)
        
        for key in keys:
            self._keyboard.press(key)
        
        self._random_sleep_ms(press_ms, variance)
        
        for key in keys:
            self._keyboard.release(key)
        
        self._random_sleep_ms(release_ms, variance)
    
    def _random_sleep_ms(self, base_ms, variance_ms):
        """
        Random delay
        
        Args:
            base_ms: Base delay time in milliseconds
            variance_ms: Random variance in milliseconds
        """
        delay = int(random.uniform(base_ms - variance_ms, base_ms + variance_ms))
        time.sleep_ms(delay)
    
    def _handle_script(self, action, params):
        """
        Handle script action (forward to ScriptEngine)
        
        Args:
            action: Script action (upload, list, run, pause, resume, stop, delete, status)
            params: Action parameters
            
        Returns:
            dict: Response
        """
        if action == "upload":
            return self._script_engine.upload(
                name=params["name"],
                steps=params["steps"],
                loop=params.get("loop", False),
                variance_ms=params.get("variance_ms", 0)
            )
        elif action == "delete":
            return self._script_engine.delete(name=params["name"])
        elif action == "list":
            return self._script_engine.list()
        elif action == "status":
            return self._script_engine.status()
        elif action == "pause":
            return self._script_engine.pause()
        elif action == "resume":
            return self._script_engine.resume()
        elif action == "stop":
            return self._script_engine.stop()
        elif action == "run":
            return {"success": False, "message": "Use async_run for script execution"}
        
        return {"success": False, "message": f"Unknown script action: {action}"}
    
    async def async_run_script(self, name):
        """
        Async run script (for use with asyncio event loop)
        
        Args:
            name: Script name
            
        Returns:
            dict: Response
        """
        return await self._script_engine.run(name, self._keyboard)