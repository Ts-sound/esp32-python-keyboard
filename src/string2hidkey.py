# String to HID Key Mapping (String as key, HID code as value)
string_to_hid_key = {
    'a': 0x04, 'b': 0x05, 'c': 0x06, 'd': 0x07, 'e': 0x08, 'f': 0x09, 'g': 0x0A, 'h': 0x0B,
    'i': 0x0C, 'j': 0x0D, 'k': 0x0E, 'l': 0x0F, 'm': 0x10, 'n': 0x11, 'o': 0x12, 'p': 0x13,
    'q': 0x14, 'r': 0x15, 's': 0x16, 't': 0x17, 'u': 0x18, 'v': 0x19, 'w': 0x1A, 'x': 0x1B,
    'y': 0x1C, 'z': 0x1D, '1': 0x1E, '2': 0x1F, '3': 0x20, '4': 0x21, '5': 0x22, '6': 0x23,
    '7': 0x24, '8': 0x25, '9': 0x26, '0': 0x27,

    'Enter': 0x28, 'Escape': 0x29, 'Backspace': 0x2A, 'Tab': 0x2B, 'Space': 0x2C, 
    '-': 0x2D, '=': 0x2E, '[': 0x2F, ']': 0x30, '\\': 0x31, '#': 0x32, ';': 0x33, '\'': 0x34, 
    '`': 0x35, ',': 0x36, '.': 0x37, '/': 0x38, 
    
    'CapsLock': 0x39, 'F1': 0x3A, 'F2': 0x3B, 'F3': 0x3C, 'F4': 0x3D, 'F5': 0x3E, 'F6': 0x3F,
    'F7': 0x40, 'F8': 0x41, 'F9': 0x42, 'F10': 0x43, 'F11': 0x44, 'F12': 0x45,

    'Insert': 0x49, 'Home': 0x4A, 'PageUp': 0x4B, 'Delete': 0x4C, 'End': 0x4D, 
    'PageDown': 0x4E, 'Right': 0x4F, 'Left': 0x50, 'Down': 0x51, 'Up': 0x52,

    'NumLock': 0x53, 'NumpadSlash': 0x54, 'NumpadAsterisk': 0x55, 'NumpadMinus': 0x56,
    'NumpadPlus': 0x57, 'NumpadEnter': 0x58, 'Numpad1': 0x59, 'Numpad2': 0x5A, 
    'Numpad3': 0x5B, 'Numpad4': 0x5C, 'Numpad5': 0x5D, 'Numpad6': 0x5E, 
    'Numpad7': 0x5F, 'Numpad8': 0x60, 'Numpad9': 0x61, 'Numpad0': 0x62, 'NumpadDot': 0x63,

    'CtrlLeft': 0xE0, 'ShiftLeft': 0xE1, 'AltLeft': 0xE2, 'MetaLeft': 0xE3, 
    'CtrlRight': 0xE4, 'ShiftRight': 0xE5, 'AltRight': 0xE6, 'MetaRight': 0xE7
}

# Example function to get HID code from string
def get_hid_code_from_string(key_str):
    return string_to_hid_key.get(key_str, 'Unknown Key')

# Example usage
# key_str = 'a'  # Example: 'a'
# print(f"String '{key_str}' corresponds to HID code: {get_hid_code_from_string(key_str)}")

# key_str = 'Enter'  # Example: 'Enter'
# print(f"String '{key_str}' corresponds to HID code: {get_hid_code_from_string(key_str)}")
