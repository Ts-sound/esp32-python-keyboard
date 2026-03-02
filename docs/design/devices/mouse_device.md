# MouseDevice - 鼠标设备设计

## 概述

提供高级鼠标 API，封装 HID 驱动，支持按钮控制、移动和滚轮。

## 类结构

```
MouseDevice
├── _hid: MouseDriver
└── _buttons: [b1, b2, b3]
```

## 核心方法

### 基本操作

| 方法 | 描述 |
|------|------|
| `start()` | 启动鼠标 |
| `start_advertising()` | 开始 BLE 广播 |
| `is_connected()` | 检查连接状态 |

### 按钮控制

| 方法 | 描述 |
|------|------|
| `click(button)` | 点击按钮 |
| `press(button)` | 按下按钮 |
| `release(button)` | 释放按钮 |

按钮参数：`left`, `middle`, `right`

### 移动和滚动

| 方法 | 描述 |
|------|------|
| `move(x, y)` | 移动鼠标 |
| `scroll(steps)` | 滚动滚轮 |

## 按钮映射

```
left   → _buttons[0]
middle → _buttons[1]
right  → _buttons[2]
```

## 移动范围

X/Y 轴位移：-127 到 127（单次报告限制）

## 使用示例

```python
from devices.mouse_device import MouseDevice

mouse = MouseDevice()
mouse.start()
mouse.start_advertising()

# 点击
mouse.click('left')
mouse.click('right')

# 移动
mouse.move(50, 30)

# 滚动
mouse.scroll(1)    # 向上
mouse.scroll(-1)   # 向下

# 拖拽
mouse.press('left')
mouse.move(100, 0)
mouse.release('left')
```
