"""
JSON 协议解析器

解析和验证 JSON 命令。
"""

import json

VALID_TYPES = {'keyboard', 'script'}
VALID_KEYBOARD_ACTIONS = {'press', 'release', 'release_all', 'type', 'sequence'}
VALID_SCRIPT_ACTIONS = {'upload', 'list', 'run', 'pause', 'resume', 'stop', 'delete', 'status'}


def _error(message):
    """返回错误响应"""
    return {'success': False, 'message': message}


def _success(data):
    """返回成功响应"""
    result = {'success': True}
    result.update(data)
    return result


class ProtocolParser:
    """JSON 协议解析器"""

    def parse(self, json_str):
        """解析 JSON 字符串"""
        try:
            data = json.loads(json_str)
        except Exception:
            return _error('Invalid JSON')

        if not isinstance(data, dict):
            return _error('Invalid JSON')

        if 'v' not in data:
            return _error('Missing field: v')

        if 'type' not in data:
            return _error('Missing field: type')

        if 'action' not in data:
            return _error('Missing field: action')

        cmd_type = data['type']
        action = data['action']

        if cmd_type not in VALID_TYPES:
            return _error(f'Unknown type: {cmd_type}')

        valid_actions = VALID_KEYBOARD_ACTIONS if cmd_type == 'keyboard' else VALID_SCRIPT_ACTIONS
        if action not in valid_actions:
            return _error(f'Unknown action: {action}')

        return _success({
            'type': cmd_type,
            'action': action,
            'params': data.get('params', {})
        })