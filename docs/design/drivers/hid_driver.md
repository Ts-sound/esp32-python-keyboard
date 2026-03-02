# HIDDriver - HID 驱动设计

## 概述

封装 MicroPythonBLEHID 库，提供统一的 HID 键盘/鼠标驱动 API。

## 类结构

### HIDDriver (键盘)

```
HIDDriver
├── _keyboard: HIDKeyboard
└── _connected: bool
```

### MouseDriver (鼠标)

```
MouseDriver
└── _mouse: HIDMouse
```

## HIDDriver 核心方法

| 方法 | 描述 |
|------|------|
| `start()` | 启动 HID 服务 |
| `start_advertising()` | 开始广播 |
| `stop_advertising()` | 停止广播 |
| `send_keys(keys, modifiers)` | 发送按键 |
| `release_all()` | 释放所有键 |
| `set_battery_level(level)` | 设置电量 |
| `notify_battery_level()` | 通知电量 |
| `is_connected()` | 检查连接 |

## MouseDriver 核心方法

| 方法 | 描述 |
|------|------|
| `start()` | 启动鼠标服务 |
| `start_advertising()` | 开始广播 |
| `set_buttons(b1, b2, b3)` | 设置按钮 |
| `move(x, y, wheel)` | 移动/滚动 |
| `is_connected()` | 检查连接 |

## 按键发送流程

```python
send_keys([0x04], {'left_shift': 1})
  ↓
_keyboard.set_keys(0x04)
_keyboard.set_modifiers(left_shift=1)
  ↓
_keyboard.notify_hid_report()
  ↓
BLE 广播
```

## 修饰符掩码

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

## 状态管理

BLE 连接状态通过回调更新：
```python
_keyboard.set_state_change_callback(self._on_state_change)

def _on_state_change(self):
    state = self._keyboard.get_state()
    # DEVICE_CONNECTED / DEVICE_DISCONNECTED
```

## 依赖

- `hid_services.Keyboard`
- `hid_services.Mouse`
- `lib/hid_services.py` (MicroPythonBLEHID 库)

## 使用示例

```python
from drivers.hid_driver import HIDDriver

hid = HIDDriver("ESP32-Keyboard")
hid.start()
hid.start_advertising()

# 发送按键
hid.send_keys([0x04])  # 'a'
hid.release_all()

# 组合键
hid.send_keys([0x04], {'left_shift': 1})  # 'A'
```
