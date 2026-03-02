# ESP32 Keyboard 系统架构

## 概述

ESP32 Python Keyboard 是一个基于 MicroPython 的 BLE HID 键盘系统，采用分层架构设计，支持 WiFi 远程控制和自动按键功能。

## 分层架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        应用层 (app/)                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  keyboard_app.py - 应用入口，协调所有服务和设备            │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                        服务层 (services/)                        │
│  ┌──────────────────────┐    ┌──────────────────────────────┐  │
│  │  wifi_service.py     │    │  rf4_service.py              │  │
│  │  - WiFi 连接管理       │    │  - RF4 自动按键               │  │
│  │  - TCP 服务器         │    │  - JIG/PULL 模式             │  │
│  │  - 客户端通信         │    │  - 消息队列控制              │  │
│  └──────────────────────┘    └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                        设备层 (devices/)                         │
│  ┌──────────────────────┐    ┌──────────────────────────────┐  │
│  │  keyboard_device.py  │    │  mouse_device.py             │  │
│  │  - 单键按下/释放       │    │  - 鼠标按钮控制              │  │
│  │  - 多键无冲 (6 键)      │    │  - 鼠标移动/滚动             │  │
│  │  - 字符串发送         │    │                              │  │
│  └──────────────────────┘    └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                        驱动层 (drivers/)                         │
│  ┌──────────────────────┐    ┌──────────────────────────────┐  │
│  │  msg_queue.py        │    │  hid_driver.py               │  │
│  │  - 发布/订阅消息队列   │    │  - HID 键盘/鼠标封装          │  │
│  │  - 固定缓冲区防溢出   │    │  - 电池电量管理              │  │
│  │                      │    │                              │  │
│  │  led_driver.py       │    │                              │  │
│  │  - LED 状态指示        │    │                              │  │
│  └──────────────────────┘    └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                        配置层 (config/)                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  config.py - 统一配置管理                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                        工具层 (utils/)                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  hid_mapper.py - HID 键码映射表                           │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓ ↑
┌─────────────────────────────────────────────────────────────────┐
│                        硬件抽象层                                │
│  ┌──────────────────────┐    ┌──────────────────────────────┐  │
│  │  MicroPythonBLEHID   │    │  machine/network/socket      │  │
│  │  (hid_services.py)   │    │  (MicroPython 内置)          │  │
│  └──────────────────────┘    └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## 模块依赖关系

```
keyboard_app
├── MessageQueue
├── KeyboardDevice
│   └── HIDDriver
│       └── hid_services.Keyboard
├── WiFiService
│   └── network, socket
└── RF4Service
    └── KeyboardDevice

HIDDriver
├── hid_services
└── HID_KEYMAP (utils/hid_mapper)

MouseDriver
└── hid_services.Mouse
```

## 数据流

### 1. WiFi 远程控制流程

```
客户端发送命令 → WiFiService.recv_data() 
              → msg_queue.publish("wifi/raw", cmd)
              → RF4Service._handle_command()
              → KeyboardDevice.press/release()
              → HIDDriver.send_keys()
              → BLE 广播
```

### 2. HID 报告发送流程

```
应用层调用 press('a')
  ↓
KeyboardDevice._send_report()
  ↓
HIDDriver.send_keys([0x04])
  ↓
hid_services.set_keys(0x04)
  ↓
hid_services.notify_hid_report()
  ↓
BLE 广播 → 主机接收
```

### 3. 消息队列流程

```
发布者 (WiFiService)
  ↓ publish("topic", msg)
MessageQueue
  ├─→ 加入队列 (poll 可获取)
  └─→ invoke_subscribers()
       ↓
       订阅者回调 (RF4Service)
```

## 状态管理

### KeyboardApp 状态
- `_running`: 运行标志
- 组件引用：`_msg_queue`, `_keyboard`, `_wifi`, `_rf4`

### WiFiService 状态
- `_connected`: WiFi 连接状态
- `_socket`: TCP 服务器 socket
- `_client`: 客户端连接

### RF4Service 状态
- `_state`: IDLE / JIG / PULL
- `_time_press`, `_time_release`: 时序参数

### HIDDriver 状态
- `_connected`: BLE 连接状态（通过回调更新）

## 错误处理

所有模块采用统一的错误处理模式：

```python
try:
    # 业务逻辑
    pass
except Exception as e:
    print(f"[ERROR] Module.method: {e}")
    import sys
    sys.print_exception(e)
    return False  # 或 None
```

## 配置管理

所有配置参数集中在 `config/config.py`：

| 类别 | 配置项 |
|------|--------|
| WiFi | SSID, PASSWORD, PORT, TIMEOUT |
| RF4 | JIG_PRESS_MS, JIG_RELEASE_MS, PULL_*, VARIANCE |
| HID | DEVICE_NAME, BATTERY_LEVEL, REPORT_INTERVAL |
| 硬件 | LED_PIN, BLINK_* |
| 系统 | MAIN_LOOP_INTERVAL_MS, DEBUG_ENABLED |
