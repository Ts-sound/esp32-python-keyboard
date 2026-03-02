# KeyboardDevice - 键盘设备设计

## 概述

提供高级键盘 API，封装 HID 驱动，支持多键无冲和字符串发送。

## 类结构

```
KeyboardDevice
├── _hid: HIDDriver
└── _pressed_keys: list
```

## 核心方法

### 基本操作

| 方法 | 描述 |
|------|------|
| `start()` | 启动键盘 |
| `start_advertising()` | 开始 BLE 广播 |
| `stop_advertising()` | 停止广播 |
| `is_connected()` | 检查连接状态 |

### 按键控制

| 方法 | 描述 |
|------|------|
| `press(key)` | 按下按键 |
| `release(key)` | 释放按键 |
| `release_all()` | 释放所有按键 |
| `send_string(text)` | 发送字符串 |

### 修饰键

| 方法 | 描述 |
|------|------|
| `set_modifiers(**kwargs)` | 设置修饰键 |

### 电池管理

| 方法 | 描述 |
|------|------|
| `set_battery_level(level)` | 设置电量 (0-100) |
| `notify_battery_level()` | 通知主机电量 |

## 多键无冲

支持最多 6 键同时按下：
```python
press('a')      # _pressed_keys = [0x04]
press('s')      # _pressed_keys = [0x04, 0x16]
press('d')      # _pressed_keys = [0x04, 0x16, 0x07]
_send_report()  # 发送 3 键组合
```

## 字符串发送

逐字符发送，自动处理大小写：
```python
send_string("Hi")
# 'H' → shift+h → release
# 'i' → i → release
```

## HID 键码映射

基于 `utils/hid_mapper.HID_KEYMAP`：

| 类别 | 示例 |
|------|------|
| 字母 | a-z (0x04-0x1d) |
| 数字 | 0-9 (0x1e-0x27) |
| 功能键 | enter, escape, backspace |
| 修饰键 | ctrlleft, shiftleft, altleft |
| 功能键 | F1-F12 (0x3a-0x45) |
| 方向键 | up, down, left, right |
| 小键盘 | numpad0-9, numpadenter |

## 使用示例

```python
from devices.keyboard_device import KeyboardDevice

kbd = KeyboardDevice()
kbd.start()
kbd.start_advertising()

# 单键
kbd.press('a')
kbd.release('a')

# 组合键
kbd.press('ctrl')
kbd.press('s')
kbd.release_all()

# 字符串
kbd.send_string("Hello World")
```
