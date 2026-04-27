"""
Script Engine Module

Manages script storage and basic operations.
"""

from config import MAX_SCRIPTS


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