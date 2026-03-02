# HIDMapper - HID 键码映射设计

## 概述

提供完整的 HID 键盘键码映射表，基于 USB HID Usage Tables 标准。

## 映射表

### HID_KEYMAP

#### 字母键 (0x04-0x1d)
```
a: 0x04, b: 0x05, ..., z: 0x1d
```

#### 数字键 (0x1e-0x27)
```
1: 0x1e, 2: 0x1f, ..., 0: 0x27
```

#### 功能键
| 键名 | 码值 |
|------|------|
| enter | 0x28 |
| escape | 0x29 |
| backspace | 0x2a |
| tab | 0x2b |
| space | 0x2c |

#### 符号键
| 键名 | 码值 |
|------|------|
| - | 0x2d |
| = | 0x2e |
| [ | 0x2f |
| ] | 0x30 |
| \\\\ | 0x31 |
| # | 0x32 |
| ; | 0x33 |
| ' | 0x34 |
| ` | 0x35 |
| , | 0x36 |
| . | 0x37 |
| / | 0x38 |

#### 功能键 F1-F12 (0x3a-0x45)

#### 方向键
| 键名 | 码值 |
|------|------|
| right | 0x4f |
| left | 0x50 |
| down | 0x51 |
| up | 0x52 |

#### 修饰键 (0xe0-0xe7)
| 键名 | 码值 |
|------|------|
| ctrlleft | 0xe0 |
| shiftleft | 0xe1 |
| altleft | 0xe2 |
| metaleft | 0xe3 |
| ctrlright | 0xe4 |
| shiftright | 0xe5 |
| altright | 0xe6 |
| metaright | 0xe7 |

### HID_MODIFIERS

| 修饰符 | 掩码 |
|--------|------|
| left_control | 0x01 |
| left_shift | 0x02 |
| left_alt | 0x04 |
| left_gui | 0x08 |
| right_control | 0x10 |
| right_shift | 0x20 |
| right_alt | 0x40 |
| right_gui | 0x80 |

## 工具函数

### get_hid_code(key_str)
获取 HID 键码：
```python
get_hid_code('a')   # → 0x04
get_hid_code('enter')  # → 0x28
```

### get_modifier_code(modifier_str)
获取修饰键掩码：
```python
get_modifier_code('left_shift')  # → 0x02
```

### parse_key_string(key_str)
解析组合键：
```python
parse_key_string('Ctrl+S')  
# → (0x16, 0x01)  # 's' + left_control

parse_key_string('A')  
# → (0x04, 0x02)  # 'a' + left_shift
```

## 使用示例

```python
from utils.hid_mapper import HID_KEYMAP, parse_key_string

# 直接查表
code = HID_KEYMAP['enter']  # 0x28

# 解析组合键
key_code, mod_mask = parse_key_string('Ctrl+Z')
```

## 参考

- USB HID Usage Tables v1.12
- MicroPythonBLEHID hid_services
