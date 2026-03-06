"""
HID Keycode Mapping Utility

Provides complete HID keyboard keycode mapping table.
Based on USB HID Usage Tables standard.
"""

HID_KEYMAP = {
    'a': 0x04, 'b': 0x05, 'c': 0x06, 'd': 0x07, 'e': 0x08,
    'f': 0x09, 'g': 0x0a, 'h': 0x0b, 'i': 0x0c, 'j': 0x0d,
    'k': 0x0e, 'l': 0x0f, 'm': 0x10, 'n': 0x11, 'o': 0x12,
    'p': 0x13, 'q': 0x14, 'r': 0x15, 's': 0x16, 't': 0x17,
    'u': 0x18, 'v': 0x19, 'w': 0x1a, 'x': 0x1b, 'y': 0x1c,
    'z': 0x1d,
    
    '1': 0x1e, '2': 0x1f, '3': 0x20, '4': 0x21, '5': 0x22,
    '6': 0x23, '7': 0x24, '8': 0x25, '9': 0x26, '0': 0x27,
    
    'enter': 0x28,
    'escape': 0x29,
    'backspace': 0x2a,
    'tab': 0x2b,
    ' ': 0x2c,
    'space': 0x2c,
    
    '-': 0x2d, 'equal': 0x2e,
    '[': 0x2f, ']': 0x30,
    '\\\\': 0x31, '#': 0x32,
    ';': 0x33, "'": 0x34,
    '`': 0x35, ',': 0x36,
    '.': 0x37, '/': 0x38,
    
    'capslock': 0x39,
    'f1': 0x3a, 'f2': 0x3b, 'f3': 0x3c, 'f4': 0x3d,
    'f5': 0x3e, 'f6': 0x3f, 'f7': 0x40, 'f8': 0x41,
    'f9': 0x42, 'f10': 0x43, 'f11': 0x44, 'f12': 0x45,
    
    'insert': 0x49, 'home': 0x4a, 'pageup': 0x4b,
    'delete': 0x4c, 'end': 0x4d, 'pagedown': 0x4e,
    'right': 0x4f, 'left': 0x50, 'down': 0x51, 'up': 0x52,
    
    'numlock': 0x53, 'numpadslash': 0x54, 'numpadasterisk': 0x55,
    'numpadminus': 0x56, 'numpadplus': 0x57, 'numpadenter': 0x58,
    'numpad1': 0x59, 'numpad2': 0x5a, 'numpad3': 0x5b,
    'numpad4': 0x5c, 'numpad5': 0x5d, 'numpad6': 0x5e,
    'numpad7': 0x5f, 'numpad8': 0x60, 'numpad9': 0x61,
    'numpad0': 0x62, 'numpaddot': 0x63,
    
    'ctrlleft': 0xe0, 'shiftleft': 0xe1, 'altleft': 0xe2, 'metaleft': 0xe3,
    'ctrlright': 0xe4, 'shiftright': 0xe5, 'altright': 0xe6, 'metaright': 0xe7,
}


HID_MODIFIERS = {
    'left_control': 0x01,
    'left_shift': 0x02,
    'left_alt': 0x04,
    'left_gui': 0x08,
    'right_control': 0x10,
    'right_shift': 0x20,
    'right_alt': 0x40,
    'right_gui': 0x80,
}


def get_hid_code(key_str):
    """
    Get HID keycode
    
    Args:
        key_str: Key name string
        
    Returns:
        int: HID keycode, None for unknown keys
    """
    return HID_KEYMAP.get(key_str.lower())


def get_modifier_code(modifier_str):
    """
    Get modifier keycode
    
    Args:
        modifier_str: Modifier key name
        
    Returns:
        int: Modifier bitmask
    """
    return HID_MODIFIERS.get(modifier_str.lower(), 0)


def parse_key_string(key_str):
    """
    Parse key string, return keycode and modifier
    
    Args:
        key_str: Key string (e.g., 'A', 'Ctrl+S')
        
    Returns:
        tuple: (key_code, modifier_mask)
    """
    modifier_mask = 0
    key = key_str
    
    if '+' in key_str:
        parts = key_str.split('+')
        key = parts[-1]
        modifiers = parts[:-1]
        
        for mod in modifiers:
            mod = mod.strip().lower()
            if mod in ('ctrl', 'control'):
                modifier_mask |= HID_MODIFIERS['left_control']
            elif mod == 'shift':
                modifier_mask |= HID_MODIFIERS['left_shift']
            elif mod in ('alt', 'option'):
                modifier_mask |= HID_MODIFIERS['left_alt']
            elif mod in ('gui', 'win', 'meta'):
                modifier_mask |= HID_MODIFIERS['left_gui']
    
    key_code = get_hid_code(key.strip())
    return key_code, modifier_mask
