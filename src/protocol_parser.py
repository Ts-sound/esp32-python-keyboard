"""
JSON 协议解析器

解析和验证 JSON 命令。
"""

import json

VALID_TYPES = {'keyboard', 'script'}
VALID_KEYBOARD_ACTIONS = {'press', 'release', 'release_all', 'type', 'sequence'}
VALID_SCRIPT_ACTIONS = {'upload', 'list', 'run', 'pause', 'resume', 'stop', 'delete', 'status', 'save'}


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

        params = data.get('params', {})
        
        if cmd_type == 'keyboard':
            params_result = self._validate_keyboard_params(action, params)
            if not params_result['success']:
                return params_result
            params = params_result['params']
        elif cmd_type == 'script':
            params_result = self._validate_script_params(action, params)
            if not params_result['success']:
                return params_result
            params = params_result['params']

        return _success({
            'type': cmd_type,
            'action': action,
            'params': params
        })

    def _validate_keyboard_params(self, action, params):
        """验证键盘命令参数"""
        if action in ('press', 'release'):
            return self._validate_press_release_params(params)
        elif action == 'release_all':
            return _success({'params': params})
        elif action == 'type':
            return self._validate_type_params(params)
        elif action == 'sequence':
            return self._validate_sequence_params(params)
        return _success({'params': params})

    def _validate_press_release_params(self, params):
        """验证 press/release 参数"""
        if 'keys' not in params:
            return _error('Missing param: keys')
        keys = params['keys']
        if not isinstance(keys, list):
            return _error('Invalid param: keys must be array')
        if len(keys) == 0:
            return _error('Invalid param: keys must be non-empty')
        return _success({'params': params})

    def _validate_type_params(self, params):
        """验证 type 参数"""
        if 'text' not in params:
            return _error('Missing param: text')
        text = params['text']
        if not isinstance(text, str):
            return _error('Invalid param: text must be string')
        result_params = dict(params)
        if 'delay_ms' not in result_params:
            result_params['delay_ms'] = 50
        return _success({'params': result_params})

    def _validate_sequence_params(self, params):
        """验证 sequence 参数"""
        if 'steps' not in params:
            return _error('Missing param: steps')
        steps = params['steps']
        if not isinstance(steps, list):
            return _error('Invalid param: steps must be array')
        if len(steps) == 0:
            return _error('Invalid param: steps must be non-empty')
        
        result_params = dict(params)
        
        if 'loop' not in result_params:
            result_params['loop'] = False
        if 'variance_ms' not in result_params:
            result_params['variance_ms'] = 0
        
        default_variance = result_params['variance_ms']
        validated_steps = []
        for step in steps:
            step_result = self._validate_sequence_step(step, default_variance)
            if not step_result['success']:
                return step_result
            validated_steps.append(step_result['step'])
        result_params['steps'] = validated_steps
        
        return _success({'params': result_params})

    def _validate_sequence_step(self, step, default_variance):
        """验证 sequence step"""
        if 'keys' not in step:
            return _error('Missing param: keys in step')
        keys = step['keys']
        if not isinstance(keys, list) or len(keys) == 0:
            return _error('Invalid param: keys in step must be non-empty array')
        
        result_step = dict(step)
        if 'press_ms' not in result_step:
            result_step['press_ms'] = 50
        if 'release_ms' not in result_step:
            result_step['release_ms'] = 50
        if 'variance_ms' not in result_step:
            result_step['variance_ms'] = default_variance
        
        return _success({'step': result_step})

    def _validate_script_params(self, action, params):
        """验证脚本命令参数"""
        if action == 'upload':
            return self._validate_script_upload_params(params)
        elif action in ('run', 'delete'):
            return self._validate_script_run_delete_params(params)
        elif action in ('list', 'status', 'pause', 'resume', 'stop', 'save'):
            return _success({'params': params})
        return _success({'params': params})

    def _validate_script_upload_params(self, params):
        """验证 script upload 参数"""
        if 'name' not in params:
            return _error('Missing param: name')
        name = params['name']
        if not isinstance(name, str):
            return _error('Invalid param: name must be string')
        
        if 'steps' not in params:
            return _error('Missing param: steps')
        steps = params['steps']
        if not isinstance(steps, list):
            return _error('Invalid param: steps must be array')
        if len(steps) == 0:
            return _error('Invalid param: steps must be non-empty')
        
        result_params = dict(params)
        
        if 'loop' not in result_params:
            result_params['loop'] = False
        if 'variance_ms' not in result_params:
            result_params['variance_ms'] = 0
        
        default_variance = result_params['variance_ms']
        validated_steps = []
        for step in steps:
            step_result = self._validate_sequence_step(step, default_variance)
            if not step_result['success']:
                return step_result
            validated_steps.append(step_result['step'])
        result_params['steps'] = validated_steps
        
        return _success({'params': result_params})

    def _validate_script_run_delete_params(self, params):
        """验证 script run/delete 参数"""
        if 'name' not in params:
            return _error('Missing param: name')
        name = params['name']
        if not isinstance(name, str):
            return _error('Invalid param: name must be string')
        return _success({'params': params})