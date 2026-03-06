# ESP32 Keyboard 系统架构

## 概述

ESP32 Python Keyboard 是一个基于 MicroPython 的 BLE HID 键盘系统，采用分层架构设计，支持 WiFi 远程控制和自动按键功能。

## 分层架构图

```mermaid
flowchart LR
    subgraph App["应用层"]
        KA["keyboard_app.py<br/>应用入口，协调所有服务和设备"]
    end
    
    subgraph Services["服务层"]
        WS["wifi_service.py<br/>WiFi 连接管理<br/>TCP 服务器<br/>客户端通信"]
        RS["rf4_service.py<br/>RF4 自动按键<br/>JIG/PULL 模式<br/>消息队列控制"]
    end
    
    subgraph Devices["设备层"]
        KD["keyboard_device.py<br/>单键按下/释放<br/>多键无冲 (6 键)<br/>字符串发送"]
    end
    
    subgraph Drivers["驱动层"]
        LD["led_driver.py<br/>LED 状态指示"]
        MQ["msg_queue.py<br/>发布/订阅消息队列<br/>固定缓冲区防溢出"]
    end
    
    subgraph Config["配置层"]
        CFG["config.py<br/>统一配置管理"]
    end
    
    subgraph Utils["工具层"]
        HM["hid_mapper.py<br/>HID 键码映射表"]
    end
    
    subgraph Hardware["硬件抽象层"]
        MPH["MicroPythonBLEHID<br/>(hid_services.py)"]
        NATIVE["machine/network/socket<br/>(MicroPython 内置)"]
    end
    
    KA --> WS
    KA --> RS
    WS --> MQ
    RS --> MQ
    RS --> KD
    KA --> KD
    KD --> MPH
    WS --> NATIVE
    KD --> HM
    LD --> CFG
```

## 模块依赖关系

```mermaid
flowchart LR
    KA[keyboard_app] --> MQ[MessageQueue]
    KA --> KD[KeyboardDevice]
    KA --> WS[WiFiService]
    KA --> RS[RF4Service]
    
    KD --> HSK[hid_services.Keyboard]
    KD --> HM[HID_KEYMAP]
    
    WS --> NET[network, socket]
    
    RS --> KD
    RS --> MQ
    
    LD[LEDDriver] --> CFG[config]
```

## 数据流

### 1. WiFi 远程控制流程

```mermaid
sequenceDiagram
    participant Client as 客户端
    participant WS as WiFiService
    participant MQ as MessageQueue
    participant RS as RF4Service
    participant KD as KeyboardDevice
    participant HD as HIDDriver
    participant BLE as BLE 广播
    
    Client->>WS: 发送命令
    WS->>MQ: publish("wifi/raw", cmd)
    MQ->>RS: _handle_command()
    RS->>KD: press/release()
    KD->>HD: send_keys()
    HD->>BLE: 广播 HID 报告
```

### 2. HID 报告发送流程

```mermaid
flowchart TD
    A["press('a')"] --> B["KeyboardDevice._send_report()"]
    B --> C["HIDDriver.send_keys([0x04])"]
    C --> D["hid_services.set_keys(0x04)"]
    D --> E["hid_services.notify_hid_report()"]
    E --> F["BLE 广播"]
    F --> G["主机接收"]
```

### 3. 消息队列流程

```mermaid
flowchart TD
    Pub[发布者<br/>WiFiService] -->|publish| MQ[MessageQueue]
    MQ --> Q[加入队列<br/>poll 可获取]
    MQ --> Sub[invoke_subscribers]
    Sub --> CB[订阅者回调<br/>RF4Service]
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

所有配置参数集中在 `src/config.py`：

| 类别 | 配置项 |
|------|--------|
| WiFi | SSID, PASSWORD, PORT, TIMEOUT |
| RF4 | JIG_PRESS_MS, JIG_RELEASE_MS, PULL_*, VARIANCE |
| HID | DEVICE_NAME, BATTERY_LEVEL, REPORT_INTERVAL |
| 硬件 | LED_PIN, BLINK_* |
| 系统 | MAIN_LOOP_INTERVAL_MS, DEBUG_ENABLED |

## 项目结构

```
esp32-python-keyboard/
├── boot.py              # ESP32 启动脚本（设备根目录）
├── src/
│   ├── main.py          # 应用入口
│   ├── config.py        # 统一配置
│   ├── keyboard_app.py  # 应用协调器
│   ├── keyboard_device.py   # 键盘设备（直接使用 hid_services）
│   ├── hid_mapper.py        # HID 映射表
│   ├── led_driver.py        # LED 驱动
│   ├── msg_queue.py         # 消息队列
│   ├── wifi_service.py      # WiFi 服务
│   └── rf4_service.py       # RF4 服务
```
